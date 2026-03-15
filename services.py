from db_config import get_connection
from model import User
from sqlalchemy import select


def get_user(username: str = None, user_id: int = None):

    with get_connection() as db:

        if username:
            stmt = select(User).where(User.username == username)

        elif user_id:
            stmt = select(User).where(User.id == user_id)

        else:
            return None

        result = db.execute(stmt)
        user = result.scalar_one_or_none()

    return user