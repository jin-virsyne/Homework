
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from models import *

# ---------------------------- Question Repository --------------------------- #
class QuestionRepository(SQLAlchemyAsyncRepository[QuestionModel]):
    model_type = QuestionModel

async def provide_questions_repo(db_session: AsyncSession) -> QuestionRepository:
    return QuestionRepository(session=db_session)


async def provide_question_details_repo(db_session: AsyncSession) -> QuestionRepository:
    return QuestionRepository(
        statement=select(QuestionModel).options(selectinload(QuestionModel.choices)),
        session=db_session,
    )
    

# ----------------------------- Choice Repository ---------------------------- #
class ChoiceRepository(SQLAlchemyAsyncRepository[ChoiceModel]):
    model_type = ChoiceModel
    
async def provide_choices_repo(db_session: AsyncSession) -> ChoiceRepository:
    return ChoiceRepository(session=db_session)