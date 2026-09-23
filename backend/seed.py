from app import app
from models import db, Rover


with app.app_context():

    db.create_all()

    existing_rover = Rover.query.first()

    if existing_rover:
        print("Rover already exists!")
        print("Rover ID:", existing_rover.id)

    else:
        rover = Rover(
            name="Agricultural Rover 01",
            status="online",
            battery=100
        )

        db.session.add(rover)
        db.session.commit()

        print("Rover created successfully!")
        print("Rover ID:", rover.id)
        