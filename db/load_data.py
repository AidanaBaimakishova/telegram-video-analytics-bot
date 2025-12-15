import json
from pathlib import Path
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session

from db.database import SessionLocal
from db.models import Video, VideoSnapshot


DATA_PATH = Path("data/videos.json")


def parse_datetime(value: str) -> datetime:
    """Парсинг ISO datetime с таймзоной"""
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Файл {DATA_PATH} не найден")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    session: Session = SessionLocal()

    try:
        for video_data in data["videos"]:
            video = Video(
                id=UUID(video_data["id"]),
                creator_id=UUID(video_data["creator_id"]),
                video_created_at=parse_datetime(video_data["video_created_at"]),
                views_count=video_data["views_count"],
                likes_count=video_data["likes_count"],
                comments_count=video_data["comments_count"],
                reports_count=video_data["reports_count"],
                created_at=parse_datetime(video_data["created_at"]),
                updated_at=parse_datetime(video_data["updated_at"]),
            )

            session.add(video)

            for snapshot_data in video_data.get("snapshots", []):
                snapshot = VideoSnapshot(
                    id=UUID(snapshot_data["id"]),
                    video_id=UUID(snapshot_data["video_id"]),
                    views_count=snapshot_data["views_count"],
                    likes_count=snapshot_data["likes_count"],
                    comments_count=snapshot_data["comments_count"],
                    reports_count=snapshot_data["reports_count"],
                    delta_views_count=snapshot_data["delta_views_count"],
                    delta_likes_count=snapshot_data["delta_likes_count"],
                    delta_comments_count=snapshot_data["delta_comments_count"],
                    delta_reports_count=snapshot_data["delta_reports_count"],
                    created_at=parse_datetime(snapshot_data["created_at"]),
                    updated_at=parse_datetime(snapshot_data["updated_at"]),
                )

                session.add(snapshot)

        session.commit()
        print("✅ Данные успешно загружены в БД")

    except Exception as e:
        session.rollback()
        print("❌ Ошибка при загрузке данных:")
        raise e

    finally:
        session.close()


if __name__ == "__main__":
    load_data()
