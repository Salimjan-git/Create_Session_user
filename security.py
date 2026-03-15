from db_config import get_connection
from model import SessionModel
import uuid
import hashlib

SECRET_KEY = "my#super@secret!key"


def hash_password(password: str) -> str:
    data = SECRET_KEY + password
    return hashlib.sha256(data.encode()).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password



def generate_token(user_id: int) -> str:

    token_str = str(uuid.uuid4())

    token = SessionModel(
        token=token_str,
        user_id=user_id
    )

    with get_connection() as db:
        db.add(token)
        db.commit()

    return token_str