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
    print("Its working!!!!")
    genai.configure(api_key=GEMINI_API_KEY)
    
    comment = get_object_or_404(Comment, id=comment_id)

    model = genai.GenerativeModel("gemini-1.5-flash")
    user = CustomUser.objects.get(id=user_id)
    response = model.generate_content(f"Я створюю сайт на якому можна створювати пости і коментувати ці пости, мені потрібно, щоб ти автоматично відповів на коментар: {comment_content} від користувача: {user}. Напиши тільки одною відповіддю, можеш писати розширено, придержуючись одної думки!")
    CommentReply(
        comment=comment,
        content=response.text,
        is_ai=True,
    )
    # return response.text

@router.post("/create_comment", response=CommentSchema)  
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
        
    auto_reply_text = None
    if post.user.auto_reply_enabled:
        delay_minutes = post.user.auto_reply_delay  
        # auto_reply_text = generate_auto_reply(comment.content, request.user)
        
        # Виклик Celery таски із затримкою
        generate_auto_reply.apply_async(
            args=[comment.id, comment.content, request.user.id], 
            countdown=delay_minutes * 60
        )

    return {
            "post_id": post.id,
            "user_id": request.user.id,
            "content": profanity_check['censored'],
            'status': "success",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "message": "Comment contains profanity and was censored."
        }

@router.get('/comment/{post_id}', response=CommentSchema)
def get_comment(request, post_id: int):
    comments = Comment.objects.filter(post=post_id)
    return comments

@router.put('/comment/{comment_id}', response=CommentSchema)
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
    return comment

@router.delete("/comment/{comment_id}", response=CommentSchema)
def delete_comment(request, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return {"success": True}

def list_comments_for_post(request, post_id: int):
    comments = Comment.objects.filter(post_id=post_id)
    
    if comments.exists():
        return {"comments": list(comments)}
    else:
        return {"message": "No comments found for this post."}

@router.get("/users/{user_id}/comments", response=list[CommentSchema])
def list_comments_for_user(request, user_id: int):
    comments = Comment.objects.filter(user_id=user_id)
    
    if comments.exists():
        return {"comments": list(comments)}
    else:
        return {"message": "No comments found for this user."}