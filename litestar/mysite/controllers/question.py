from __future__ import annotations

from pydantic import parse_obj_as

from litestar import get
from litestar.contrib.repository.filters import LimitOffset
from litestar.controller import Controller
from litestar.di import Provide
from litestar.handlers.http_handlers.decorators import delete, patch, post
from litestar.pagination import OffsetPagination
from litestar.params import Parameter

from repositories import *

class QuestionController(Controller):
    """Question CRUD"""
    dependencies = {"questions_repo": Provide(provide_questions_repo)}

    @get(path="/questions")
    async def list_questions(
        self,
        questions_repo: QuestionRepository,
        limit_offset: LimitOffset,
    ) -> OffsetPagination[Question]:
        """List questions."""
        results, total = await questions_repo.list_and_count(limit_offset)
        return OffsetPagination[Question](
            items=parse_obj_as(list[Question], results),
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @post(path="/questions")
    async def create_question(
        self,
        questions_repo: QuestionRepository,
        data: QuestionCreate,
    ) -> Question:
        """Create a new question."""
        obj = await questions_repo.add(
            QuestionModel(**data.dict(exclude_unset=True, by_alias=False, exclude_none=True)),
        )
        await questions_repo.session.commit()
        return Question.from_orm(obj)

    # we override the questions_repo to use the version that joins the Choice in
    @get(path="/questions/{question_id:uuid}", dependencies={"questions_repo": Provide(provide_question_details_repo)})
    async def get_question(
        self,
        questions_repo: QuestionRepository,
        question_id: UUID = Parameter(
            title="Question ID",
            description="The question to retrieve.",
        ),
    ) -> Question:
        """Get an existing question."""
        obj = await questions_repo.get(question_id)
        return Question.from_orm(obj)

    @patch(
        path="/questions/{question_id:uuid}",
        dependencies={"questions_repo": Provide(provide_question_details_repo)},
    )
    async def update_question(
        self,
        questions_repo: QuestionRepository,
        data: QuestionUpdate,
        question_id: UUID = Parameter(
            title="Question ID",
            description="The question to update.",
        ),
    ) -> Question:
        """Update an question."""
        raw_obj = data.dict(exclude_unset=True, by_alias=False, exclude_none=True)
        raw_obj.update({"id": question_id})
        obj = await questions_repo.update(QuestionModel(**raw_obj))
        await questions_repo.session.commit()
        return Question.from_orm(obj)

    @delete(path="/questions/{question_id:uuid}")
    async def delete_question(
        self,
        questions_repo: QuestionRepository,
        question_id: UUID = Parameter(
            title="Question ID",
            description="The question to delete.",
        ),
    ) -> None:
        """Delete a question from the system."""
        _ = await questions_repo.delete(question_id)
        await questions_repo.session.commit()