from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Rover(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="offline")
    battery = db.Column(db.Float, default=0)


class Telemetry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rover_id = db.Column(
        db.Integer,
        db.ForeignKey("rover.id"),
        nullable=False
    )

    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    battery = db.Column(db.Float)

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rover_id = db.Column(
        db.Integer,
        db.ForeignKey("rover.id"),
        nullable=False
    )

    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rover_id = db.Column(
        db.Integer,
        db.ForeignKey("rover.id"),
        nullable=False
    )

    detection_type = db.Column(db.String(100))
    confidence = db.Column(db.Float)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rover_id = db.Column(
        db.Integer,
        db.ForeignKey("rover.id"),
        nullable=False
    )

    treatment_type = db.Column(db.String(100))
    status = db.Column(db.String(50))

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rover_id = db.Column(
        db.Integer,
        db.ForeignKey("rover.id"),
        nullable=False
    )

    name = db.Column(db.String(100))
    status = db.Column(
        db.String(50),
        default="pending"
    )

    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)


class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    rover_id = db.Column(
        db.Integer,
        db.ForeignKey("rover.id"),
        nullable=False
    )

    command = db.Column(
        db.String(100),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    executed_at = db.Column(db.DateTime)
    