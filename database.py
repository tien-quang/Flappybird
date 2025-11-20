import json
import os

DB_FILE = "players.json"

def load_or_create_player(name):
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}
    if name not in data:
        data[name] = {"best_score": 0}
    return data.get(name, {"best_score": 0})

def update_player_score(name, score):
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}
    if name not in data:
        data[name] = {"best_score": score}
    else:
        if score > data[name]["best_score"]:
            data[name]["best_score"] = score
    with open(DB_FILE, "w") as f:
        json.dump(data, f)
    return data[name]["best_score"]

def get_highest_score():
    if not os.path.exists(DB_FILE):
        return 0
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    if not data:
        return 0
    return max(player["best_score"] for player in data.values())
