import math
import json
def calculate_xp(xp):
    level=int(math.sqrt(xp/100))+1
    return level

def difficulty_multiplier(question,xp):
    with open(question, "r") as file:
        data = json.load(file)
    diffuculty = data["set_info"]["level"]
    if diffuculty=="medium":
        xp=xp*1.3
    elif diffuculty=="hard":
        xp=xp*1.7
    return int(xp)
def convert_level(user):
    with open(f"users/{user}.json", "r") as file:
        data = json.load(file)
        xp=data.get("xp", 0)
        level=calculate_xp(xp)
        data["level"]=level
    with open(f"users/{user}.json", "w") as file:
        json.dump(data, file, indent=4)

def actual_xp(xp):
    lvl=int(math.sqrt(xp/100))+1
    lvl-=1
    lvl=lvl*lvl
    lvl=lvl*100
    actual_exp=xp-lvl

    if actual_exp>1000000:
        actual_exp=round(actual_exp/1000000,2)
        actual_exp=str(actual_exp)+" M"
    elif actual_exp>1000:
        actual_exp=round(actual_exp/1000,2)
        actual_exp=str(actual_exp)+" K"
    return actual_exp

def required_xp(user):
    with open(f"users/{user}.json", "r") as file:
        data = json.load(file)
        xp=data.get("xp", 0)
        lvl=data.get("level", 1)
        prev_xp = ((lvl-1)**2) * 100
        next_xp = (lvl**2) * 100
        progress = (xp - prev_xp) / (next_xp - prev_xp)
    return progress

def xp_required(user):
    with open(f"users/{user}.json", "r") as file:
        data = json.load(file)
        xp=data.get("xp", 0)
        next_xp = (data.get("level", 1)**2) * 100
        requirement=next_xp-xp
    return requirement