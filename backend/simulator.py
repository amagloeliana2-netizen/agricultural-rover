import random
import time
from datetime import datetime

import requests


API_URL = "http://127.0.0.1:5000"

ROVER_ID = 1


def generate_telemetry():
    return {
        "rover_id": ROVER_ID,
        "temperature": round(random.uniform(27.0, 32.0), 1),
        "humidity": round(random.uniform(60.0, 85.0), 1),
        "battery": round(random.uniform(70.0, 100.0), 1)
    }


def generate_location():
    return {
        "rover_id": ROVER_ID,
        "latitude": round(
            5.6037 + random.uniform(-0.0020, 0.0020),
            6
        ),
        "longitude": round(
            -0.1870 + random.uniform(-0.0020, 0.0020),
            6
        )
    }


def send_telemetry():
    telemetry = generate_telemetry()

    response = requests.post(
        f"{API_URL}/api/telemetry",
        json=telemetry
    )

    print(
        datetime.now().strftime("%H:%M:%S"),
        "Telemetry:",
        response.status_code,
        telemetry
    )


def send_location():
    location = generate_location()

    response = requests.post(
        f"{API_URL}/api/location",
        json=location
    )

    print(
        datetime.now().strftime("%H:%M:%S"),
        "GPS:",
        response.status_code,
        location
    )


def main():
    print("Agricultural Rover Simulator")
    print("----------------------------")
    print("Rover ID:", ROVER_ID)
    print("Sending simulated data...")
    print()

    while True:
        try:
            send_telemetry()
            send_location()

            print()

            time.sleep(5)

        except requests.exceptions.ConnectionError:
            print(
                "Could not connect to Flask backend."
            )
            print(
                "Make sure python app.py is running."
            )
            print()

            time.sleep(5)

        except KeyboardInterrupt:
            print()
            print("Simulator stopped.")
            break


if __name__ == "__main__":
    main()