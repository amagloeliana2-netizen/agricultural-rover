
import os

from datetime import datetime

from flask import Flask, jsonify, request, send_from_directory

from models import (
    db,
    Rover,
    Telemetry,
    Location,
    Detection,
    Treatment,
    Mission
)


BACKEND_FOLDER = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(BACKEND_FOLDER)

FRONTEND_FOLDER = os.path.join(
    PROJECT_ROOT,
    "frontend"
)

FRONTEND_JS_FOLDER = os.path.join(
    FRONTEND_FOLDER,
    "js"
)

FRONTEND_CSS_FOLDER = os.path.join(
    FRONTEND_FOLDER,
    "css"
)

DATABASE_PATH = os.path.join(
    BACKEND_FOLDER,
    "rover.db"
)


app = Flask(
    __name__,
    static_folder=FRONTEND_FOLDER,
    static_url_path=""
)


app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{DATABASE_PATH.replace(os.sep, '/')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


@app.route("/")
def home():
    return send_from_directory(
        FRONTEND_FOLDER,
        "index.html"
    )


@app.route("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory(
        FRONTEND_JS_FOLDER,
        filename
    )


@app.route("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory(
        FRONTEND_CSS_FOLDER,
        filename
    )


@app.route("/api/status", methods=["GET"])
def status():
    rover = Rover.query.first()

    if rover:
        return jsonify({
            "rover": rover.name,
            "status": rover.status,
            "battery": rover.battery
        })

    return jsonify({
        "rover": "Agricultural Rover",
        "status": "offline",
        "battery": 0
    })


@app.route("/api/telemetry", methods=["POST"])
def receive_telemetry():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    if data.get("rover_id") is None:
        return jsonify({
            "error": "rover_id is required"
        }), 400

    telemetry = Telemetry(
        rover_id=data.get("rover_id"),
        temperature=data.get("temperature"),
        humidity=data.get("humidity"),
        battery=data.get("battery")
    )

    db.session.add(telemetry)
    db.session.commit()

    return jsonify({
        "message": "Telemetry received successfully",
        "data": {
            "id": telemetry.id,
            "rover_id": telemetry.rover_id,
            "temperature": telemetry.temperature,
            "humidity": telemetry.humidity,
            "battery": telemetry.battery,
            "timestamp": (
                telemetry.timestamp.isoformat()
                if telemetry.timestamp
                else None
            )
        }
    }), 201


@app.route("/api/telemetry", methods=["GET"])
def get_telemetry():
    records = (
        Telemetry.query
        .order_by(Telemetry.timestamp.desc())
        .all()
    )

    return jsonify([
        {
            "id": record.id,
            "rover_id": record.rover_id,
            "temperature": record.temperature,
            "humidity": record.humidity,
            "battery": record.battery,
            "timestamp": (
                record.timestamp.isoformat()
                if record.timestamp
                else None
            )
        }
        for record in records
    ])


@app.route("/api/location", methods=["POST"])
def receive_location():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    if data.get("rover_id") is None:
        return jsonify({
            "error": "rover_id is required"
        }), 400

    if (
        data.get("latitude") is None
        or data.get("longitude") is None
    ):
        return jsonify({
            "error": "latitude and longitude are required"
        }), 400

    location = Location(
        rover_id=data.get("rover_id"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude")
    )

    db.session.add(location)
    db.session.commit()

    return jsonify({
        "message": "Location received successfully",
        "data": {
            "id": location.id,
            "rover_id": location.rover_id,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timestamp": (
                location.timestamp.isoformat()
                if location.timestamp
                else None
            )
        }
    }), 201


@app.route("/api/location", methods=["GET"])
def get_location():
    records = (
        Location.query
        .order_by(Location.timestamp.desc())
        .all()
    )

    return jsonify([
        {
            "id": record.id,
            "rover_id": record.rover_id,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "timestamp": (
                record.timestamp.isoformat()
                if record.timestamp
                else None
            )
        }
        for record in records
    ])


@app.route("/api/detections", methods=["POST"])
def receive_detection():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    if data.get("rover_id") is None:
        return jsonify({
            "error": "rover_id is required"
        }), 400

    if not data.get("detection_type"):
        return jsonify({
            "error": "detection_type is required"
        }), 400

    if data.get("confidence") is None:
        return jsonify({
            "error": "confidence is required"
        }), 400

    detection = Detection(
        rover_id=data.get("rover_id"),
        detection_type=data.get("detection_type"),
        confidence=data.get("confidence"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude")
    )

    db.session.add(detection)
    db.session.commit()

    return jsonify({
        "message": "Detection received successfully",
        "data": {
            "id": detection.id,
            "rover_id": detection.rover_id,
            "detection_type": detection.detection_type,
            "confidence": detection.confidence,
            "latitude": detection.latitude,
            "longitude": detection.longitude,
            "timestamp": (
                detection.timestamp.isoformat()
                if detection.timestamp
                else None
            )
        }
    }), 201


@app.route("/api/detections", methods=["GET"])
def get_detections():
    records = (
        Detection.query
        .order_by(Detection.timestamp.desc())
        .all()
    )

    return jsonify([
        {
            "id": record.id,
            "rover_id": record.rover_id,
            "detection_type": record.detection_type,
            "confidence": record.confidence,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "timestamp": (
                record.timestamp.isoformat()
                if record.timestamp
                else None
            )
        }
        for record in records
    ])


@app.route("/api/treatments", methods=["POST"])
def create_treatment():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    if data.get("rover_id") is None:
        return jsonify({
            "error": "rover_id is required"
        }), 400

    if not data.get("treatment_type"):
        return jsonify({
            "error": "treatment_type is required"
        }), 400

    treatment = Treatment(
        rover_id=data.get("rover_id"),
        treatment_type=data.get("treatment_type"),
        status=data.get("status", "pending"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude")
    )

    db.session.add(treatment)
    db.session.commit()

    return jsonify({
        "message": "Treatment recorded successfully",
        "data": {
            "id": treatment.id,
            "rover_id": treatment.rover_id,
            "treatment_type": treatment.treatment_type,
            "status": treatment.status,
            "latitude": treatment.latitude,
            "longitude": treatment.longitude,
            "timestamp": (
                treatment.timestamp.isoformat()
                if treatment.timestamp
                else None
            )
        }
    }), 201


@app.route("/api/treatments", methods=["GET"])
def get_treatments():
    records = (
        Treatment.query
        .order_by(Treatment.timestamp.desc())
        .all()
    )

    return jsonify([
        {
            "id": record.id,
            "rover_id": record.rover_id,
            "treatment_type": record.treatment_type,
            "status": record.status,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "timestamp": (
                record.timestamp.isoformat()
                if record.timestamp
                else None
            )
        }
        for record in records
    ])


@app.route("/api/missions", methods=["POST"])
def create_mission():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    if data.get("rover_id") is None:
        return jsonify({
            "error": "rover_id is required"
        }), 400

    if not data.get("name"):
        return jsonify({
            "error": "name is required"
        }), 400

    mission = Mission(
        rover_id=data.get("rover_id"),
        name=data.get("name"),
        status=data.get("status", "pending")
    )

    if mission.status == "running":
        mission.started_at = datetime.utcnow()

    db.session.add(mission)
    db.session.commit()

    return jsonify({
        "message": "Mission created successfully",
        "data": {
            "id": mission.id,
            "rover_id": mission.rover_id,
            "name": mission.name,
            "status": mission.status,
            "started_at": (
                mission.started_at.isoformat()
                if mission.started_at
                else None
            ),
            "completed_at": None
        }
    }), 201


@app.route("/api/missions", methods=["GET"])
def get_missions():
    records = (
        Mission.query
        .order_by(Mission.id.desc())
        .all()
    )

    return jsonify([
        {
            "id": record.id,
            "rover_id": record.rover_id,
            "name": record.name,
            "status": record.status,
            "started_at": (
                record.started_at.isoformat()
                if record.started_at
                else None
            ),
            "completed_at": (
                record.completed_at.isoformat()
                if record.completed_at
                else None
            )
        }
        for record in records
    ])


@app.route(
    "/api/missions/<int:mission_id>",
    methods=["PUT"]
)
def update_mission(mission_id):
    mission = db.session.get(
        Mission,
        mission_id
    )

    if not mission:
        return jsonify({
            "error": "Mission not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    if "name" in data:
        mission.name = data["name"]

    if "status" in data:
        mission.status = data["status"]

        if mission.status == "running":
            if mission.started_at is None:
                mission.started_at = datetime.utcnow()

        if mission.status == "completed":
            mission.completed_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        "message": "Mission updated successfully",
        "data": {
            "id": mission.id,
            "rover_id": mission.rover_id,
            "name": mission.name,
            "status": mission.status,
            "started_at": (
                mission.started_at.isoformat()
                if mission.started_at
                else None
            ),
            "completed_at": (
                mission.completed_at.isoformat()
                if mission.completed_at
                else None
            )
        }
    })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )