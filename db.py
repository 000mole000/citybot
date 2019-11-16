import json


def open_db(db):
    passports = open(db, "r", encoding="utf-8")
    passports_str = passports.read()
    data = json.loads(passports_str)
    passports.close()
    return data


def update_db(db, data):
    add_user = open(db, "w", encoding="utf-8")
    data = json.dumps(data)
    add_user.write(data)
    add_user.close()
