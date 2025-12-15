from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True)
    creator_id = Column(UUID(as_uuid=True), nullable=False)

    video_created_at = Column(DateTime(timezone=True), nullable=False)

    views_count = Column(Integer, nullable=False)
    likes_count = Column(Integer, nullable=False)
    comments_count = Column(Integer, nullable=False)
    reports_count = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    # связь 1 видео -> много снапшотов
    snapshots = relationship(
        "VideoSnapshot",
        back_populates="video",
        cascade="all, delete-orphan"
    )


class VideoSnapshot(Base):
    __tablename__ = "video_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True)

    video_id = Column(
        UUID(as_uuid=True),
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=False
    )

    views_count = Column(Integer, nullable=False)
    likes_count = Column(Integer, nullable=False)
    comments_count = Column(Integer, nullable=False)
    reports_count = Column(Integer, nullable=False)

    delta_views_count = Column(Integer, nullable=False)
    delta_likes_count = Column(Integer, nullable=False)
    delta_comments_count = Column(Integer, nullable=False)
    delta_reports_count = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    # обратная связь
    video = relationship(
        "Video",
        back_populates="snapshots"
    )
