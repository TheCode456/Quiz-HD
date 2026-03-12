import json

def ensure_user_structure(path):

    with open(path, "r") as f:
        data = json.load(f)

    default = {
        "username": "",
        "password": "",
        "xp": 0,
        "level": 1,
        "quizzes_played": 0,
        "stats": {
            "correct": 0,
            "wrong": 0,
            "skipped": 0
        },
        "last_quiz": {
            "quiz_name": None,
            "correct": 0,
            "wrong": 0,
            "skipped": 0,
            "xp": 0
        },
        "quizzes_completed":[
            None
        ]
    }

    # add missing top level keys
    for key in default:
        if key not in data:
            data[key] = default[key]

    # stats keys
    for key in default["stats"]:
        if key not in data["stats"]:
            data["stats"][key] = 0

    # last quiz keys
    for key in default["last_quiz"]:
        if key not in data["last_quiz"]:
            data["last_quiz"][key] = default["last_quiz"][key]

    quiz_completed=data["quizzes_completed"]
    for i in range(len(quiz_completed)):
        # skip None values before calling replace
        if quiz_completed[i] is not None:
            quiz_completed[i]=quiz_completed[i].replace("assets/questions/","")
    data["quizzes_completed"]=quiz_completed

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    return data