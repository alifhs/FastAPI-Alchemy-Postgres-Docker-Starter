from sqlalchemy.orm import Session
import models
import schemas
from redis_service import redis_client as redis
import json
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    user_data =  redis.get(f"user:{user_id}")
    if user_data:
        # If user data is found in cache, return it
        print("from redis", user_data)
        return json.loads(user_data)

    # If user data is not in cache, fetch it from the database
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user:
        # Cache the user data in Redis
        redis.set(f"user:{user_id}", json.dumps(user.to_dict()))

    return user
