from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import post, user

# creates models in database
models.Base.metadata.create_all(bind=engine)

# creates an instance for FastAPI
app = FastAPI()

# register routers
app.include_router(post.router)
app.include_router(user.router)
