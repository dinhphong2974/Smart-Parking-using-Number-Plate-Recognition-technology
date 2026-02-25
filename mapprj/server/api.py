from flask import Flask, request, jsonify
from flask_cors import CORS
from .storage import load_positions, save_positions
app = Flask(__name__); CORS(app); positions = []
@app.route('/update', methods=['POST'])
def update_position():
    data = request.get_json(force=True)
    lat, lon = data.get("lat"), data.get("lng")
    device_id = data.get("device_id", "unknown")
    timestamp = data.get("time", "unknown")
    if lat is None or lon is None:
        return jsonify({"error": "Thiếu lat/lon"}), 400
    new_pos = {"lat": lat, "lon": lon, "device_id": device_id, "time": timestamp}
    positions.append(new_pos); save_positions(positions)
    return jsonify({"status": "ok"}), 200
@app.route('/positions.json')
def get_positions(): return jsonify(load_positions())
def run_server():
    global positions; positions = load_positions()
    app.run(host="0.0.0.0", port=5000, threaded=True)
