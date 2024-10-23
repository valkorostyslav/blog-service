from django.db import models
from django.conf import settings
from posts.models import Post

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_blocked = models.BooleanField(default=False)
    is_auto_reply = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'
    
class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Користувач може бути null для AI-відповідей
    content = models.TextField(null=False)
    is_ai = models.BooleanField(default=False)  # Додайте це поле, щоб вказати, чи відповідь від AI
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{"AI" if self.is_ai else "User"} reply to {self.comment}'