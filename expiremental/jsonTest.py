import json
import time


def import_data(filename):
    with open(f"{filename}.json", "r") as f:
        return json.loads(f.read())


def export_data(filename, data):
    with open(f"{filename}.json", "w") as f:
        json.dump(data, f, indent=4)


def check_user_id(user_id):
    if str(user_id) in json_data["warned_users"]:
        return True
    else:
        return False


def add_user(user_id):
    json_data["warned_users"][str(user_id)] = {"time":time.time(), "count":1}


def remove_user(user_id):
    json_data["warned_users"].pop(user_id)


def increase_count(user_id):
    json_data["warned_users"][str(user_id)]["count"] += 1

if __name__ == "__main__":
    json_data = import_data("test")
    if check_user_id(2):
        increase_count(2)
    export_data("test", json_data)
