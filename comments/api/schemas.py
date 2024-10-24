from ninja import Schema
from datetime import datetime
from typing import Optional

from pydantic import ConfigDict

class CommentSchema(Schema):
    post_id: int
    user_id: int
    content: str
    status: str
    ai_response: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(orm_mode=True)
    
class CreateCommentSchema(Schema):
    post_id: int
    content: str
    
    model_config = ConfigDict(orm_mode=True)
    
class UpdateCommentSchema(Schema):
    content: Optional[str] = None