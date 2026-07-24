from flask import Blueprint, render_template, request

from ...data.bones import BONES, CATEGORY_LABELS
from ...models import Attempt
from ...utils import get_client_ip

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    ip = get_client_ip(request)
    attempts_count = Attempt.query.filter_by(ip_address=ip).count()
    best = (
        Attempt.query.filter_by(ip_address=ip)
        .order_by(Attempt.score_percent.desc())
        .first()
    )
    return render_template(
        "index.html",
        attempts_count=attempts_count,
        best_score=round(best.score_percent, 1) if best else None,
    )


@main_bp.route("/glosario")
def glossary():
    grouped = {}
    for key, bone in BONES.items():
        grouped.setdefault(bone["category"], []).append({**bone, "key": key})
    return render_template("glossary.html", grouped=grouped, category_labels=CATEGORY_LABELS)
