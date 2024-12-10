from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

DB_FILE = "database.json"
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as db_file:
        json.dump({"devices": {}, "applications": {}}, db_file)  # Initialize JSON structure

# Load configuration and database
with open("config.json") as config_file:
    config = json.load(config_file)

with open(DB_FILE) as db_file:
    database = json.load(db_file)

CHIRPSTACK_API_URL = config["chirpstack_api_url"]
CHIRPSTACK_API_TOKEN = config["api_token"]

# Save the updated database to the file
def save_database():
    with open(DB_FILE, "w") as db_file:
        json.dump(database, db_file, indent=4)

@app.route("/device/<alias>", methods=["GET"])
def forward_device_call(alias):
    device_info = database["devices"].get(alias)
    if not device_info:
        return jsonify({"error": "Alias not found"}), 404
    return jsonify(device_info), 200

@app.route("/api/devices", methods=["GET"])
def get_device_call():
    query_param = request.args.to_dict()
    headers = {
        "Authorization": f"Bearer {CHIRPSTACK_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(
        f"{CHIRPSTACK_API_URL}/api/devices",
        headers=headers,
        params=query_param
    )
    return jsonify(response.json()), response.status_code

@app.route("/api/devices", methods=["POST"])
def create_device():
    data = request.json

    headers = {
        "Authorization": f"Bearer {CHIRPSTACK_API_TOKEN}",
        "Content-Type": "application/json"
    }
    # Send request to ChirpStack to create the device
    response = requests.post(
        f"{CHIRPSTACK_API_URL}/api/devices",
        headers=headers,
        json=data
    )

    if response.status_code == 200 or response.status_code == 201:
        # Store the new device in the database
        alias = data["name"]
        deveui = data["DevEUI"]
        application_id = data["applicationID"]

        # Save device information
        database["devices"][alias] = {"DevEUI": deveui, "applicationID": application_id}

        # Save applicationID if not already in the database
        app_alias = f"application{application_id}"
        if app_alias not in database["applications"]:
            database["applications"][app_alias] = application_id

        save_database()

        return jsonify({"message": "Device created successfully", "alias": alias, "DevEUI": deveui}), 201
    else:
        return jsonify({"error": "Failed to create device", "details": response.json()}), response.status_code

@app.route("/api/applications", methods=["GET"])
def get_applications():
    return jsonify(database.get("applications", {})), 200

if __name__ == "__main__":
    app.run(debug=True)


