from fastapi import FastAPI, HTTPException, status, Request, Response, Cookie, Depends
import uvicorn
from model import *
from db_config import get_connection
from security import hash_password, verify_password, generate_token
from services import *


app = FastAPI()


def get_current_user(session_token:Request):
    session_token = session_token.cookies.get("auth_token")
    with get_connection() as db:
        if not session_token:
            raise HTTPException(status_code=401, detail="Not authenticated")

        session = db.query(SessionModel).filter(SessionModel.token == session_token).first()
        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")

        return session.user


@app.get("/say_hello")
async def say_hello(user:None = Depends(get_current_user)):
    return {"message": "Hello world!"}


@app.post("/register")
async def add_user(username:str, password:str, confirm_password:str):
    if password != confirm_password:
        raise HTTPException(detail="Passwords don't match", status_code=status.HTTP_400_BAD_REQUEST )
    hash_passowrd = hash_password(password=password) 
    new_user = User(username=username, password=hash_passowrd)
    with get_connection() as db:
        user=db.query(User).filter(User.username==username).first()
        if user:
            raise HTTPException(detail="User already exists", status_code=status.HTTP_400_BAD_REQUEST)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return new_user

@app.post("/login")
async def login_user(response:Response, username: str, password: str):
    user_exists = get_user(username=username)
    if user_exists is not None:
        print("test", user_exists.password, user_exists.username)
        print(type(password))
        is_password_correct = verify_password(password=password, hashed_password=user_exists.password)
        if not is_password_correct:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
        token = generate_token(user_id=user_exists.id)
        response.set_cookie("auth_token", token.token)
        return {"msg":"Use loged In"}
    return HTTPException(detail="Invalid credentials or user not found", status_code=status.HTTP_400_BAD_REQUEST)
        
    
@app.post("/logout")
async def logout_view(respose:Response, user = Depends(get_current_user)):
    respose.delete_cookie("auth_token")
    return "Logged out"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)