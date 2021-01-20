import json

with open("models/models.json") as file:
    data = json.load(file)

    HP_REGEN_AMOUNT = data['hp_regen']['amount']
    HP_REGEN_INTERVAL = data['hp_regen']['interval']
    PLAYER_HP = data['player']['hp']
    PLAYER_STRENGTH = data['player']['strength']
    PLAYER_DEFENSE = data['player']['defense']
