from db_config import get_connection
from model import User
from sqlalchemy import select



def get_user(username: str=None, user_id:int=None):
    user = None
    with get_connection() as db:
        if username:
            user = db.query(User).filter(User.username==username).first()
        if user_id:
            user = db.query(User).filter(User.id==user_id).first()
    
    if not user:
        return None
    return user
    