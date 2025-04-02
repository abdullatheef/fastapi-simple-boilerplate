from datetime import datetime
from typing import Annotated
import uuid as uuid_pkg

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class SamplePostBase(BaseModel):
    title: Annotated[str, Field(min_length=2, max_length=30, examples=["This is my post"])]


class SamplePost(TimestampSchema, SamplePostBase, UUIDSchema, PersistentDeletion):
    created_by_user_id: uuid_pkg.UUID


class SamplePostRead(BaseModel):
    id: uuid_pkg.UUID
    title: Annotated[str, Field(min_length=2, max_length=30, examples=["This is my post"])]
    created_by_user_id: uuid_pkg.UUID
    created_at: datetime


class SamplePostCreate(SamplePostBase):
    model_config = ConfigDict(extra="forbid")


class SamplePostCreateInternal(SamplePostCreate):
    created_by_user_id: uuid_pkg.UUID


class SamplePostUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Annotated[str | None, Field(min_length=2, max_length=30, examples=["This is my updated post"], default=None)]



class SamplePostUpdateInternal(SamplePostUpdate):
    pass


class SamplePostDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
