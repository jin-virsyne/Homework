from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from litestar.contrib.sqlalchemy.base import UUIDAuditBase, UUIDBase


class BaseModel(_BaseModel):
    """Extend Pydantic's BaseModel to enable ORM mode"""
    model_config = {"from_attributes": True}


class QuestionModel(UUIDBase):
    __tablename__ = "question"
    question_text: Mapped[str]
    pub_date: Mapped[date]
    choices: Mapped[list[ChoiceModel]] = relationship(back_populates="question", lazy="noload")

class ChoiceModel(UUIDAuditBase):
    __tablename__ = "choice"
    choice_text: Mapped[str]
    votes: Mapped[int]
    question_id: Mapped[UUID] = mapped_column(ForeignKey("question.id"))
    question: Mapped[QuestionModel] = relationship(lazy="joined", innerjoin=True, viewonly=True)

    
# ---------------------------- Choice Model Schema --------------------------- #
class Choice(BaseModel):
    id: UUID | None
    choice_text: str
    votes: int
    question_id: UUID
    
class ChoiceCreate(BaseModel):
    choice_text: str
    votes: int
    question_id: UUID

class ChoiceUpdate(BaseModel):
    choice_text: str | None = None
    votes: int | None = None
    question_id: UUID | None = None


# ------------------------------ Question Model Schema ------------------------------ #
class Question(BaseModel):
    id: UUID | None
    question_text: str
    pub_date: date
    choices: list[Choice] | None = None

class QuestionCreate(BaseModel):
    question_text: str
    pub_date: date

class QuestionUpdate(BaseModel):
    question_text: str | None = None
    pub_date: date | None = None