from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from src.utils.db import Base


class taskModel(Base):
    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    desc = Column(String)
    isCompleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("user_table.id", ondelete="CASCADE"))
