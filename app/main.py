from fastapi import FastAPI,Request,Body
from contextlib import asynccontextmanager
from typing import Annotated
from redis.asyncio import Redis
from redis.exceptions import ConnectionError
from app.core.config import settings
from app.worker import send_email
@asynccontextmanager
async def lifespan(app:FastAPI):
  try:
    redis_client = Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,decode_responses=True)
    await redis_client.ping()
    app.state.redis = redis_client
    print("redis conntected successfully!!!")
  except ConnectionError as e:
    print("Redis connection failed:", str(e))
    raise RuntimeError("Failed to connect to Redis") from e

  yield
  await app.state.redis.close()
    
app = FastAPI(lifespan=lifespan)


@app.post("/register/")
async def register(email:Annotated[str,Body()]):
  send_email.apply_async(args=[email])
  return {"message":f"user signup successfully!!!"}