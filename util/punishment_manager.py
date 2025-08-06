import json
import os

DATA_FILE = "data/punishments.json"

def load_data():
    if not os.path.isfile(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_punishment(guild_id, user_id, role_id, type_):
    data = load_data()
    key = f"{guild_id}-{user_id}"
    if key not in data:
        data[key] = {"roles": [], "types": []}
    if role_id not in data[key]["roles"]:
        data[key]["roles"].append(role_id)
    if type_ not in data[key]["types"]:
        data[key]["types"].append(type_)
    save_data(data)

def remove_punishment(guild_id, user_id, role_id=None):
    data = load_data()
    key = f"{guild_id}-{user_id}"
    if key in data:
        if role_id:
            if role_id in data[key]["roles"]:
                idx = data[key]["roles"].index(role_id)
                data[key]["roles"].pop(idx)
                if idx < len(data[key]["types"]):
                    data[key]["types"].pop(idx)
            if not data[key]["roles"]:
                del data[key]
        else:
            del data[key]
    save_data(data)

def get_user_roles(guild_id, user_id):
    data = load_data()
    return data.get(f"{guild_id}-{user_id}", {}).get("roles", [])