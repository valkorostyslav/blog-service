from ninja import Schema
from datetime import datetime
from typing import Optional

class CommentSchema(Schema):
    post_id: int
    user_id: int
    content: str
    ai_response: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
class CreateCommentSchema(Schema):
    post_id: int
    content: str
    
class UpdateCommentSchema(Schema):
    content: Optional[str] = None