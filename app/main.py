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
    redis_client = Redis.from_url(settings.REDIS_URL,max_connections=10,decode_responses=True)
    await redis_client.ping()
    app.state.redis = redis_client
    print("redis conntected successfully!!!")
  except ConnectionError as e:
    print("Redis connection failed:", str(e))
    raise RuntimeError("Failed to connect to Redis") from e

  yield
  if hasattr(app.state, "redis"):
    await app.state.redis.close()
    print("Redis connection closed.")
    
app = FastAPI(lifespan=lifespan)


@app.post("/register/")
async def register(email:Annotated[str,Body()]):
  send_email.apply_async(args=[email])
  return {"message":f"user signup successfully!!!"}

@app.get("/get/price/")
async def get_price(request:Request):
  redis_client = request.app.state.redis
  price = await redis_client.get("btc:price:latest")
  return {"bitcoin_price":price}