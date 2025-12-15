from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db.models import Video, VideoSnapshot

print("analytics.py loaded")

# -------- БАЗОВЫЕ МЕТРИКИ (videos) --------

def get_total_views() -> int:
    session = SessionLocal()
    try:
        result = session.query(
            func.sum(Video.views_count)
        ).scalar()
        return result or 0
    finally:
        session.close()



def get_total_likes() -> int:
    """Общее количество лайков"""
    session: Session = SessionLocal()
    try:
        result = session.query(
            func.sum(Video.likes_count)
        ).scalar()
        return result or 0
    finally:
        session.close()


def get_creator_total_views(creator_id: str) -> int:
    """Итоговые просмотры по креатору"""
    session: Session = SessionLocal()
    try:
        result = session.query(
            func.sum(Video.views_count)
        ).filter(
            Video.creator_id == creator_id
        ).scalar()
        return result or 0
    finally:
        session.close()


# -------- ДИНАМИКА / ПРИРОСТ (video_snapshots) --------

def get_total_views_growth() -> int:
    """Общий прирост просмотров за всё время"""
    session: Session = SessionLocal()
    try:
        result = session.query(
            func.sum(VideoSnapshot.delta_views_count)
        ).scalar()
        return result or 0
    finally:
        session.close()


def get_views_growth_for_period(
    start: datetime,
    end: datetime
) -> int:
    """Прирост просмотров за период"""
    session: Session = SessionLocal()
    try:
        result = session.query(
            func.sum(VideoSnapshot.delta_views_count)
        ).filter(
            VideoSnapshot.created_at >= start,
            VideoSnapshot.created_at <= end
        ).scalar()
        return result or 0
    finally:
        session.close()


def get_creator_views_growth(creator_id: str) -> int:
    """Прирост просмотров по креатору"""
    session: Session = SessionLocal()
    try:
        result = session.query(
            func.sum(VideoSnapshot.delta_views_count)
        ).join(
            Video,
            Video.id == VideoSnapshot.video_id
        ).filter(
            Video.creator_id == creator_id
        ).scalar()
        return result or 0
    finally:
        session.close()
