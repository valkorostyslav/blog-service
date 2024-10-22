from ninja import Schema

class UserCreate(Schema):
    username: str
    email: str
    password: str
    
class UserLogin(Schema):
    email: str
    password: str