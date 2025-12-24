from uuid import UUID
from sqlalchemy import func
from datetime import datetime
from db.database import SessionLocal
from db.models import Video, VideoSnapshot

TABLES = {
    "videos": Video,
    "video_snapshots": VideoSnapshot,
}

def run_aggregate(parsed: dict) -> int:
    session = SessionLocal()
    model = TABLES[parsed["table"]]

    aggregation = parsed["aggregation"]
    field = parsed.get("field")
    filters = parsed.get("filters", {})

    threshold = filters.get("threshold")

    try:
        # --- aggregation ---
        if aggregation == "count":
            if threshold:
                query = session.query(func.count(model.id))
            else:
                query = session.query(func.count()).select_from(model)

        elif aggregation == "sum" and field:
            query = session.query(func.sum(getattr(model, field)))

        else:
            return 0

        # --- creator_id ---
        creator_id = filters.get("creator_id")
        if creator_id:
            creator_id = UUID(creator_id)
            if model is Video:
                query = query.filter(Video.creator_id == creator_id)
            else:
                query = query.join(Video).filter(Video.creator_id == creator_id)

        # --- date range ---
        date_from = filters.get("date_from")
        if date_from:
            query = query.filter(model.created_at >= datetime.fromisoformat(date_from))

        date_to = filters.get("date_to")
        if date_to:
            query = query.filter(model.created_at <= datetime.fromisoformat(date_to))

        # --- threshold ---
        if threshold:
            col = getattr(model, threshold["field"])
            query = query.filter(col > threshold["value"])

        return query.scalar() or 0

    finally:
        session.close()

