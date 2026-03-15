from fastapi import FastAPI, HTTPException, Response, Depends, Cookie
from sqlalchemy import select
import uvicorn

from db_config import engine, get_connection
from model import Base, User, SessionModel, Note
from security import hash_password, verify_password, generate_token
from services import get_user


app = FastAPI(title="Notes API")


Base.metadata.create_all(bind=engine)




def get_current_user(session_token: str = Cookie(None)):

    if not session_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    with get_connection() as db:

        stmt = select(SessionModel).where(SessionModel.token == session_token)
        session = db.execute(stmt).scalar_one_or_none()

        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")

        user = db.get(User, session.user_id)

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user



@app.post("/register")
def register(username: str, password: str):

    if get_user(username=username):
        raise HTTPException(400, "User already exists")

    hashed = hash_password(password)

    new_user = User(
        username=username,
        password=hashed
    )

    with get_connection() as db:
        db.add(new_user)
        db.commit()

    return {"message": "User created"}




@app.post("/login")
def login(username: str, password: str, response: Response):

    user = get_user(username=username)

    if not user:
        raise HTTPException(404, "User not found")

    if not verify_password(password, user.password):
        raise HTTPException(400, "Wrong password")

    token = generate_token(user.id)

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True
    )

    return {"message": "Login successful"}



@app.post("/logout")
def logout(response: Response, session_token: str = Cookie(None)):

    if not session_token:
        raise HTTPException(401, "Not logged in")

    with get_connection() as db:

        stmt = select(SessionModel).where(SessionModel.token == session_token)
        session = db.execute(stmt).scalar_one_or_none()

        if session:
            db.delete(session)
            db.commit()

    response.delete_cookie("session_token")

    return {"message": "Logged out"}



@app.post("/notes")
def create_note(title: str, content: str, user: User = Depends(get_current_user)):

    note = Note(
        title=title,
        content=content,
        user_id=user.id
    )

    with get_connection() as db:
        db.add(note)
        db.commit()

    return {"message": "Note created"}



@app.get("/notes")
def get_notes(user: User = Depends(get_current_user)):

    with get_connection() as db:

        stmt = select(Note).where(Note.user_id == user.id)

        notes = db.execute(stmt).scalars().all()

    return notes




@app.get("/notes/{note_id}")
def get_note(note_id: int, user: User = Depends(get_current_user)):

    with get_connection() as db:

        stmt = select(Note).where(
            Note.id == note_id,
            Note.user_id == user.id
        )

        note = db.execute(stmt).scalar_one_or_none()

    if not note:
        raise HTTPException(404, "Note not found")

    return note



@app.put("/notes/{note_id}")
def update_note(note_id: int, title: str, content: str, user: User = Depends(get_current_user)):

    with get_connection() as db:

        stmt = select(Note).where(
            Note.id == note_id,
            Note.user_id == user.id
        )

        note = db.execute(stmt).scalar_one_or_none()

        if not note:
            raise HTTPException(404, "Note not found")

        note.title = title
        note.content = content

        db.commit()

    return {"message": "Note updated"}




@app.delete("/notes/{note_id}")
def delete_note(note_id: int, user: User = Depends(get_current_user)):

    with get_connection() as db:

        stmt = select(Note).where(
            Note.id == note_id,
            Note.user_id == user.id
        )

        note = db.execute(stmt).scalar_one_or_none()

        if not note:
            raise HTTPException(404, "Note not found")

        db.delete(note)
        db.commit()

    return {"message": "Note deleted"}


if __name__ == "__main__": 
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)