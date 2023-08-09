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

class ChoiceController(Controller):
    """Choice CRUD"""
    dependencies = {"choices_repo": Provide(provide_choices_repo)}

    @get(path="/choices")
    async def list_choices(
        self,
        choices_repo: ChoiceRepository,
        limit_offset: LimitOffset,
    ) -> OffsetPagination[Choice]:
        """List choices."""
        results, total = await choices_repo.list_and_count(limit_offset)
        return OffsetPagination[Choice](
            items=parse_obj_as(list[Choice], results),
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @post(path="/choices")
    async def create_choice(
        self,
        choices_repo: ChoiceRepository,
        data: ChoiceCreate,
    ) -> Choice:
        """Create a new choice."""
        obj = await choices_repo.add(
            ChoiceModel(**data.dict(exclude_unset=True, by_alias=False, exclude_none=True)),
        )
        await choices_repo.session.commit()
        return Choice.from_orm(obj)

    @get(path="/choices/{choice_id:uuid}")
    async def get_choice(
        self,
        choices_repo: ChoiceRepository,
        choice_id: UUID = Parameter(
            title="Choice ID",
            description="The choice to retrieve.",
        ),
    ) -> Choice:
        """Get an existing choice."""
        obj = await choices_repo.get(choice_id)
        return Choice.from_orm(obj)

    @patch(path="/choices/{choice_id:uuid}")
    async def update_choice(
        self,
        choices_repo: ChoiceRepository,
        data: ChoiceUpdate,
        choice_id: UUID = Parameter(
            title="Choice ID",
            description="The choice to update.",
        ),
    ) -> Choice:
        """Update an choice."""
        raw_obj = data.dict(exclude_unset=True, by_alias=False, exclude_none=True)
        raw_obj.update({"id": choice_id})
        obj = await choices_repo.update(ChoiceModel(**raw_obj))
        await choices_repo.session.commit()
        return Choice.from_orm(obj)

    @delete(path="/choices/{choice_id:uuid}")
    async def delete_choice(
        self,
        choices_repo: ChoiceRepository,
        choice_id: UUID = Parameter(
            title="Choice ID",
            description="The choice to delete.",
        ),
    ) -> None:
        """Delete a choice from the system."""
        _ = await choices_repo.delete(choice_id)
        await choices_repo.session.commit()