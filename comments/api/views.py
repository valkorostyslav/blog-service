from typing import List
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Router
import requests
from comments.api.schemas import CommentSchema, CreateCommentSchema, UpdateCommentSchema
from comments.models import Comment, CommentReply
from posts.models import Post
from decouple import config
import google.generativeai as genai
import os
from datetime import datetime
from celery import shared_task
from user.models import CustomUser

router = Router()

NINJAS_API_KEY = config('NINJAS_API_KEY')
GEMINI_API_KEY = config('GEMINI_API_KEY')


def check_for_obscene_language(text: str):
    api_url = f'https://api.api-ninjas.com/v1/profanityfilter?text={text}'
    response = requests.get(api_url, headers={'X-Api-Key': NINJAS_API_KEY})
    if response.status_code == requests.codes.ok:
        return response.json() 
    else:
        print("Error:", response.status_code, response.text)
        return None

@shared_task
def generate_auto_reply(comment_id, comment_content, user_id):
    genai.configure(api_key=GEMINI_API_KEY)
    
    comment = get_object_or_404(Comment, id=comment_id)

    model = genai.GenerativeModel("gemini-1.5-flash")
    user = CustomUser.objects.get(id=user_id)
    response = model.generate_content(f"I am creating a website where users can create posts and comment on these posts. I need you to automatically reply to the comment: {comment_content} from the user: {user}. Please write only one response and feel free to elaborate while staying on the same topic!")
    CommentReply(
        comment=comment,
        content=response.text,
        is_ai=True,
    )

@router.post("/create_comment", response=dict)  
def create_comment(request, payload: CreateCommentSchema):
    post = get_object_or_404(Post, id=payload.post_id)

    profanity_check = check_for_obscene_language(payload.content)

    if profanity_check and profanity_check['has_profanity']:
        comment = Comment.objects.create(
        post=post,
        user=request.user,
        content=profanity_check['censored']
        )
    else:
        comment = Comment.objects.create(
            post=post,
            user=request.user,
            content=payload.content
        )
        
    if post.user.auto_reply_enabled:
        delay_minutes = post.user.auto_reply_delay  
        
        generate_auto_reply.apply_async(
            args=[comment.id, comment.content, request.user.id], 
            countdown=delay_minutes * 60
        )

    return {
            "post_id": post.id,
            "user_id": request.user.id,
            "content": profanity_check['censored'] if profanity_check['has_profanity'] else payload.content,
            'status': "success",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

@router.get('/comment/{post_id}', response=List[dict])
def get_comment(request, post_id: int):
    comments = Comment.objects.filter(post=post_id)

    if not comments.exists():
        return []

    return [comment.to_dict() for comment in comments]

@router.put('/comment/update/{comment_id}', response=dict)
def update_comment(request, comment_id: int, payload: UpdateCommentSchema):
    comment = get_object_or_404(Comment, id=comment_id)


    if payload.content:
        profanity_check = check_for_obscene_language(payload.content)

        if profanity_check and profanity_check['has_profanity']:
            return {
                "success": False,
                "message": "Comment contains profanity.",
                "censored": profanity_check['censored']
            }
        comment.content = payload.content

    comment.save()
    return comment.to_dict()

@router.delete("/comment/delete/{comment_id}", response=dict)
def delete_comment(request, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return {"success": True}

@router.get("/users/{user_id}/comments", response=List[dict])
def list_comments_for_user(request, user_id: int):
    comments = Comment.objects.filter(user_id=user_id)
    
    return [comment.to_dict() for comment in comments] if comments.exists() else []