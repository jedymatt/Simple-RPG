from ..character import Character


class PVE:
    def __init__(self, player: Character, opponent: Character):
        self.player = player
        self.opponent = opponent

    def start(self):
        while self.player.current_hp != 0 and self.opponent.current_hp != 0:
            pass
