from ninja import Router
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from ninja_jwt.tokens import AccessToken, RefreshToken

from user.api.schemas import UserCreate, UserLogin

User = get_user_model()

router = Router()

@router.post("/register")
def register(request, payload: UserCreate):
    user = User(
        email=payload.email,
        password=make_password(payload.password),
        username=payload.username
    )
    user.save()
    return {"success": True}

@router.post("/login")
def login(request, payload: UserLogin):
    user = User.objects.filter(email=payload.email).first()
    if user and user.check_password(payload.password):
        accesss_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        return {
            "access": str(accesss_token),
            "refresh": str(refresh_token)
        }
    return {"success": False, "error": "Invalid credentials"}