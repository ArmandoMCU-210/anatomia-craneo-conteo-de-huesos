from flask import Blueprint, current_app, render_template, request

from ...data.bones import BONES, BONES_MODELS_DIR, CATEGORY_LABELS
from ...models import Attempt
from ...utils import get_client_ip, static_asset_exists

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
        model_path = f"{BONES_MODELS_DIR}/{bone['model']}"
        has_model = static_asset_exists(current_app, model_path)
        grouped.setdefault(bone["category"], []).append(
            {**bone, "key": key, "has_model": has_model, "model_path": model_path}
        )
    return render_template("glossary.html", grouped=grouped, category_labels=CATEGORY_LABELS)
