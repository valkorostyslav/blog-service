from datetime import datetime
from django.shortcuts import get_object_or_404
import requests
from ninja import NinjaAPI, Router
from comments.models import Comment
from posts.models import Post
from posts.api.schemas import PostSchema, CreatePostSchema, UpdatePostSchema
from ninja_jwt.authentication import JWTAuth
from django.db.models import Count, Q
from django.http import Http404

router = Router()

NINJAS_API_KEY = 'CmuAklblI7P1k9uqXyMX8A==4Yvc52KelAmZdFG3'

def check_for_obscene_language(text: str):
    api_url = f'https://api.api-ninjas.com/v1/profanityfilter?text={text}'
    response = requests.get(api_url, headers={'X-Api-Key': NINJAS_API_KEY})
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None
    
@router.get("/comments-daily-breakdown")
def comments_daily_breakdown(request, date_from: str, date_to: str):
    try:

        start_date = datetime.strptime(date_from, "%Y-%m-%d").date()
        end_date = datetime.strptime(date_to, "%Y-%m-%d").date()


        comments = Comment.objects.filter(created_at__date__range=(start_date, end_date))

        daily_data = (
            comments.values('created_at__date')
            .annotate(total_comments=Count('id'),
                      blocked_comments=Count('id', filter=Q(is_blocked=True))) 
            .order_by('created_at__date')
        )

        return {
            "daily_comments": list(daily_data)
        }

    except ValueError:
        return {"success": False, "message": "Invalid date format. Use YYYY-MM-DD."}

@router.get("/posts", response=list[PostSchema])  
def all_posts(request):
    posts = Post.objects.all()  
    return posts

@router.get("/posts/{post_id}", response=dict)
def post(request, post_id: int):
    try:
        post = Post.objects.get(id=post_id)
        return post.to_dict()
    except Post.DoesNotExist:
        return {"success": False, "detail": "Post not found."}

@router.post("/posts", response=dict, auth=JWTAuth())
def create_post(request, payload: CreatePostSchema):

    title_check = check_for_obscene_language(payload.title)
    content_check = check_for_obscene_language(payload.content)

    if title_check and title_check['has_profanity']:
        return {
            "success": True,
            "message": "Post contains profanity in the title.",
            "censored": title_check['censored']
        }
    
    if content_check and content_check['has_profanity']:
        return {
            "success": True, 
            "message": "Post contains profanity in the content.",
            "censored": content_check['censored']
        }
    
    user = request.auth
    post = Post.objects.create(user=user, **payload.dict())
    return PostSchema.from_orm(post).dict()

@router.put("/posts/{post_id}", response=dict)
def update_post(request, post_id: int, payload: UpdatePostSchema):
    try:
        post = get_object_or_404(Post, id=post_id)
        

        title_check = check_for_obscene_language(payload.title)
        content_check = check_for_obscene_language(payload.content)

        if title_check and title_check['has_profanity']:
            return {
                "success": False,
                "message": "Post contains profanity in the title.",
                "censored": title_check['censored']
            }

        if content_check and content_check['has_profanity']:
            return {
                "success": False, 
                "message": "Post contains profanity in the content.",
                "censored": content_check['censored']
            }
        
        for attr, value in payload.dict(exclude_none=True).items():
            setattr(post, attr, value)

        post.save()
        return {
        "success": True,
        "message": "Post was successfully updated.",
        "post": {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat()
        }
    }

    except Post.DoesNotExist:
        return {"success": False, "message": "Post not found."}
    except Exception as e:
        return {"success": False, "message": str(e)}

@router.delete("/posts/{post_id}", response=dict)
def delete_post(request, post_id: int):
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return {"success": True, "message": "Post deleted successfully."}
    except Post.DoesNotExist:
        return {"success": False, "message": "Post not found."}
    except Exception as e:
        return {"success": False, "message": str(e)}
