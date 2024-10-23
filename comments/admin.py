from django.contrib import admin
from comments.models import Comment, CommentReply

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content')  
    search_fields = ('post', 'user') 

class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'content', 'is_ai')
    search_fields = ("is_ai", 'user')

admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentReply, CommentReplyAdmin)