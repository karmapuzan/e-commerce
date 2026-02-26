from backend.app.database.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Enum
import uuid


class Category(Base):
    __tablename__ = "category"

    id = Column(
        String,
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
    )
    name = Column(String(100), nullable=True)
    slug = Column(String(100), nullable=False)
    parent_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
