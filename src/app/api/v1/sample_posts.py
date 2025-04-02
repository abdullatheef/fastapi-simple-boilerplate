from typing import Annotated, Any
import uuid as uuid_pkg

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_sample_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ...core.utils.cache import cache
from ...schemas.sample_user import SampleUserRead


from ...schemas.sample_post import SamplePostCreate, SamplePostCreateInternal, SamplePostRead, SamplePostUpdate
from ...crud.crud_sample_posts import crud_sample_post


router = APIRouter(tags=["sample_posts"])


@router.post("/sample-post", response_model=SamplePostRead, status_code=201)
async def write_post(
    request: Request,
    post: SamplePostCreate,
    current_user: Annotated[SampleUserRead, Depends(get_current_sample_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> SamplePostRead:

    post_internal_dict = post.model_dump()
    post_internal_dict["created_by_user_id"] = current_user["id"]

    post_internal = SamplePostCreateInternal(**post_internal_dict)
    created_post: SamplePostRead = await crud_sample_post.create(db=db, object=post_internal)
    return created_post



@router.get("/sample-post/{id}", response_model=SamplePostRead)
@cache(key_prefix="post_cache", resource_id_name="id")
async def read_post(
    request: Request, id: uuid_pkg.UUID, db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[SampleUserRead, Depends(get_current_sample_user)],
) -> dict:

    db_post: SamplePostRead | None = await crud_sample_post.get(
        db=db, schema_to_select=SamplePostRead, id=str(id), created_by_user_id=str(current_user["id"]), is_deleted=False
    )
    if db_post is None:
        raise NotFoundException("Post not found")

    return db_post