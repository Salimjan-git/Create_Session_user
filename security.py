from db_config import get_connection
from model import SessionModel

SECRET_KEY = "my#super@secret!key"

def hash_password(password:str):
    return SECRET_KEY+password

def verify_password(password:str, hashed_password:str):
    new_hash = hash_password(password)
    if new_hash != hashed_password:
        return False
    return True

def generate_token(user_id:int):
    token = SessionModel(user_id=user_id)
    with get_connection() as db:
        db.add(token)
        db.commit()
        db.refresh(token)
    return token
