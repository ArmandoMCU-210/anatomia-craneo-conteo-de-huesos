import json
import random
import time

from flask import Blueprint, jsonify, render_template, request, session

from ...data.bones import BONES, INTERACTIVE_KEYS, REGION_TO_KEY
from ...extensions import db
from ...models import Attempt
from ...utils import get_client_ip

game_bp = Blueprint("game", __name__)

SESSION_KEY = "skull_game"


@game_bp.route("/juego")
def start():
    keys = list(INTERACTIVE_KEYS)
    random.shuffle(keys)
    bank = [{"key": key, "name": BONES[key]["name"]} for key in keys]

    regions = [
        {"region_id": BONES[key]["region_id"], "x": BONES[key]["marker"][0], "y": BONES[key]["marker"][1]}
        for key in INTERACTIVE_KEYS
    ]

    session[SESSION_KEY] = {
        "start_time": time.time(),
        "regions": {
            BONES[key]["region_id"]: {"solved": False, "attempts": 0, "first_try_correct": None}
            for key in INTERACTIVE_KEYS
        },
    }
    session.modified = True

    return render_template("game.html", bank=bank, regions=regions, total=len(INTERACTIVE_KEYS))


@game_bp.route("/api/juego/responder", methods=["POST"])
def answer():
    data = request.get_json(silent=True) or {}
    region_id = data.get("region_id")
    bone_key = data.get("bone_key")

    game = session.get(SESSION_KEY)
    if not game or region_id not in game["regions"]:
        return jsonify({"error": "Sesión de juego inválida. Reinicia la actividad."}), 400

    region_state = game["regions"][region_id]
    if region_state["solved"]:
        return jsonify({"error": "Esta región ya fue resuelta."}), 400

    correct_key = REGION_TO_KEY.get(region_id)
    is_correct = bone_key == correct_key

    region_state["attempts"] += 1
    if region_state["first_try_correct"] is None:
        region_state["first_try_correct"] = is_correct
    if is_correct:
        region_state["solved"] = True

    session.modified = True

    solved_count = sum(1 for r in game["regions"].values() if r["solved"])
    total = len(game["regions"])

    return jsonify(
        {
            "correct": is_correct,
            "correct_bone_name": BONES[correct_key]["name"] if is_correct else None,
            "region_id": region_id,
            "solved_count": solved_count,
            "total": total,
            "all_solved": solved_count == total,
        }
    )


@game_bp.route("/api/juego/finalizar", methods=["POST"])
def finish():
    game = session.get(SESSION_KEY)
    if not game:
        return jsonify({"error": "Sesión de juego inválida. Reinicia la actividad."}), 400

    regions = game["regions"]
    total = len(regions)
    correct_first_try = sum(1 for r in regions.values() if r["first_try_correct"] is True)
    incorrect_first_try = total - correct_first_try
    score_percent = (correct_first_try / total) * 100 if total else 0
    duration = max(time.time() - game["start_time"], 0)

    details = []
    for region_id, state in regions.items():
        key = REGION_TO_KEY.get(region_id)
        details.append(
            {
                "bone": BONES[key]["name"],
                "correct": bool(state["first_try_correct"]),
                "attempts": state["attempts"],
            }
        )
    details.sort(key=lambda d: d["bone"])

    ip = get_client_ip(request)
    attempt = Attempt(
        ip_address=ip,
        duration_seconds=duration,
        total_questions=total,
        correct_count=correct_first_try,
        incorrect_count=incorrect_first_try,
        score_percent=score_percent,
        details_json=json.dumps(details, ensure_ascii=False),
    )
    db.session.add(attempt)
    db.session.commit()

    attempts_count = Attempt.query.filter_by(ip_address=ip).count()

    session.pop(SESSION_KEY, None)

    return jsonify(
        {
            "summary": attempt.to_summary(),
            "details": details,
            "attempts_count": attempts_count,
        }
    )
