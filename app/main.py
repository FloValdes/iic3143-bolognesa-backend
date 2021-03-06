from fastapi import FastAPI, Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi.middleware.cors import CORSMiddleware
from .database import database
from . import schema, models
from .config import settings

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET = "SECRET"
auth_backends = []

jwt_authentication = JWTAuthentication(secret=settings.JWT_SECRET, lifetime_seconds=settings.JWT_LIFETIME, tokenUrl="/auth/jwt/login")
auth_backends.append(jwt_authentication)

fastapi_users = FastAPIUsers(models.user_db, [jwt_authentication], schema.User, schema.UserCreate, schema.UserUpdate, schema.UserDB)

app.include_router(fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(models.on_after_register), prefix="/auth", tags=["auth"])
app.include_router(
    fastapi_users.get_reset_password_router(SECRET, after_forgot_password=models.on_after_forgot_password),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

@app.get('/')
async def hello():
    return { 'hello': 'hello' }


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
