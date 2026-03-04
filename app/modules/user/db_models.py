from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base
from app.modules.role.db_models import Role
from app.utils import TableNames


class User(Base):
    """User model. Many users belong to one role."""

    __tablename__ = TableNames.USERS.value

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    role_id: Mapped[str] = mapped_column(
        ForeignKey(f"{TableNames.ROLES.value}.id"),
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    refresh_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Many-to-one: many Users belong to one Role
    role: Mapped[Role] = relationship(
        Role,
        back_populates="users",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
