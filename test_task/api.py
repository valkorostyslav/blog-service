from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from ninja import NinjaAPI
from posts.api.views import router as posts_router
from comments.api.views import router as comments_router
from user.api.views import router as auth_router

api = NinjaExtraAPI()

api.register_controllers(NinjaJWTDefaultController)

api.add_router("", auth_router)
api.add_router("", posts_router)
api.add_router("", comments_router)