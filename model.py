from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Table, Column, UUID
import uuid

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    username:Mapped[str] = mapped_column(String(100), unique=True)
    password:Mapped[str] = mapped_column(String)
    session:Mapped["SessionModel"] = relationship("SessionModel", back_populates="user")
    
    def __repr__(self):
        return f"user: {self.username}"





class SessionModel(Base):
    __tablename__ = "sessions"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    token:Mapped[str] = mapped_column(String, default=str(uuid.uuid4()))
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    user:Mapped["User"] = relationship("User", back_populates="session")

