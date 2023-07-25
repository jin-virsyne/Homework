from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from pydantic import parse_obj_as

from litestar import get
from litestar.contrib.repository.filters import LimitOffset
from litestar.controller import Controller
from litestar.di import Provide
from litestar.handlers.http_handlers.decorators import post
from litestar.pagination import OffsetPagination
from litestar.params import Parameter, Body
from litestar.response import Template
from litestar.enums import RequestEncodingType

from repositories import *

@dataclass
class VoteDataclass:
    choice: str

class PollController(Controller):
    """Poll CRUD"""
    dependencies = {"questions_repo": Provide(provide_questions_repo)}

    @get(path="/polls")
    async def index(
        self,
        questions_repo: QuestionRepository,
        limit_offset: LimitOffset,
    ) -> Template:
        """List questions."""
        results, total = await questions_repo.list_and_count(limit_offset)
        offset = OffsetPagination[Question](
            items=parse_obj_as(list[Question], results),
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )
        return Template(
            template_name="index.html", 
            context= { "latest_question_list": offset.items }
        )


    @get(path="/polls/{question_id:uuid}", dependencies={"questions_repo": Provide(provide_question_details_repo)})
    async def detail(
        self,
        questions_repo: QuestionRepository,
        question_id: UUID = Parameter(
            title="Question ID",
            description="The question to retrieve.",
        ),
    ) -> Template:
        """Get an existing question."""
        obj = await questions_repo.get(question_id)
        return Template(
            template_name="detail.html", 
            context= { "question": Question.from_orm(obj) }
        )
    

    @post(path="/polls/{question_id:uuid}/vote", dependencies={"choices_repo": Provide(provide_choices_repo), "questions_repo": Provide(provide_question_details_repo)})
    async def vote(
        self,
        choices_repo: ChoiceRepository,
        questions_repo: QuestionRepository,
        data: Annotated[VoteDataclass, Body(media_type=RequestEncodingType.URL_ENCODED)],
        question_id: UUID = Parameter(
            title="Question ID",
            description="The question to retrieve.",
        ),
    ) -> Template:
        """Increase vote of a choice."""
        row = await choices_repo.get(data.choice)
        row_obj = Choice.from_orm(row)
        row_obj.votes += 1
        
        choiceModel = ChoiceModel()
        choiceModel.id = row_obj.id
        choiceModel.votes = row_obj.votes
      
        await choices_repo.update(choiceModel)
        await choices_repo.session.commit()

        """Get an existing question."""
        obj = await questions_repo.get(question_id)
        return Template(
            template_name="results.html", 
            context= { "question": Question.from_orm(obj) }
        )
        