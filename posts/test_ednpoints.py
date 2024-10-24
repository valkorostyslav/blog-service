import json
import pytest

from django.test import Client
from django.contrib.auth import get_user_model
from comments.models import Comment

from django.utils import timezone
from posts.models import Post


User = get_user_model()

@pytest.mark.django_db  
def test_comments_daily_breakdown():
    client = Client()

    user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
    
    post = Post.objects.create(title="Test Post", content="This is a test post.", user=user)
    
    Comment.objects.create(post=post, user=user, content='First comment today')
    Comment.objects.create(post=post, user=user, content='Second comment today')
    
    response = client.get('/api/comments-daily-breakdown', {
        'date_from': timezone.now().strftime('%Y-%m-%d'),  
        'date_to': timezone.now().strftime('%Y-%m-%d')
    })
    
    response_data = response.json()
    print(response_data)
    
    assert response.status_code == 200
    
    assert len(response_data['daily_comments']) == 1
    
    assert response_data['daily_comments'][0]['total_comments'] == 2
    
@pytest.mark.django_db
def test_create_comment():
    client = Client()

    user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
    
    post = Post.objects.create(title="Test Post", content="This is a test post.", user=user)
    
    comment_data = {
        "post_id": post.id,
        "content": "This is a test comment."
    }

    client.login(username="testuser", password="testpassword")

    response = client.post('/api/create_comment', data=json.dumps(comment_data), content_type='application/json')

    print(response.content)

    assert response.status_code == 200
    
    response_data = response.json()

    assert response_data['post_id'] == post.id
    assert response_data['user_id'] == user.id
    assert response_data['content'] == "This is a test comment."
    assert response_data['status'] == "success"

    assert Comment.objects.filter(post=post, user=user, content="This is a test comment.").exists()