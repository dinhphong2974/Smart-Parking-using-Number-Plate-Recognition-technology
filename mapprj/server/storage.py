import json, os
positions_file = os.path.join(os.path.dirname(__file__), "..", "positions.json")
def reset_positions_file():
    with open(positions_file, "w") as f: json.dump([], f)
def load_positions():
    try:
        with open(positions_file, "r") as f: return json.load(f)
    except: return []
def save_positions(positions):
    with open(positions_file, "w") as f: json.dump(positions, f)
