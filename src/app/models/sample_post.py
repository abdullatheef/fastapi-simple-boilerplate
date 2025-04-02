import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class SamplePost(BaseModel):
    __tablename__ = "sample_post"

    created_by_user_id: Mapped[uuid_pkg.UUID] = mapped_column(ForeignKey("sample_user.id"), index=True)    
    title: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
