from datetime import datetime, timezone

from .extensions import db


class Attempt(db.Model):
    """Un intento completado de la actividad de identificación de huesos del cráneo."""

    __tablename__ = "attempts"

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    duration_seconds = db.Column(db.Float, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_count = db.Column(db.Integer, nullable=False)
    incorrect_count = db.Column(db.Integer, nullable=False)
    score_percent = db.Column(db.Float, nullable=False)
    details_json = db.Column(db.Text, nullable=True)

    def to_summary(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "duration_seconds": round(self.duration_seconds, 1),
            "score_percent": round(self.score_percent, 1),
            "correct_count": self.correct_count,
            "incorrect_count": self.incorrect_count,
            "total_questions": self.total_questions,
        }
