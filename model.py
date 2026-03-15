from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime
import uuid


class Base(DeclarativeBase):
    pass




class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    password: Mapped[str] = mapped_column(String, nullable=False)

    is_admin: Mapped[bool] = mapped_column(default=False)

    sessions: Mapped["SessionModel"] = relationship(
        "SessionModel",
        back_populates="user"
    )

    notes: Mapped[list["Note"]] = relationship(
        "Note",
        back_populates="user"
    )

    def __repr__(self):
        return f"user: {self.username}"



class SessionModel(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    token: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="sessions"
    )




class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(200))

    content: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(
        DateTime
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="notes"
    )