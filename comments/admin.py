from django.contrib import admin
from comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content')  
    search_fields = ('post', 'user') 

admin.site.register(Comment, CommentAdmin)