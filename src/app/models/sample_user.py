import uuid as uuid_pkg
from datetime import UTC, datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseModel

class SampleUser(BaseModel):
    __tablename__ = "sample_user"

    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    id: Mapped[uuid_pkg.UUID] = mapped_column(default_factory=uuid_pkg.uuid4, primary_key=True, unique=True)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
