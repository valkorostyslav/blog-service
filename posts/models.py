from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    is_blocked = models.BooleanField(default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user.id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_blocked": self.is_blocked,
        }
    
    def __str__(self):
        return self.title  
