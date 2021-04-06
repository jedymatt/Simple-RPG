from ..character import Character


class PVE:
    def __init__(self, player: Character, opponent: Character):
        self.player = player
        self.opponent = opponent

    def start(self):
        while self.player.current_hp != 0 and self.opponent.current_hp != 0:
            # player attack first
            self.opponent.take_damage(self.player.strength)

            if self.opponent.current_hp <= 0:
                break

            # opponent attack second
            self.player.take_damage(self.opponent.strength)

    def zero_hp_character(self):
        return self.player if self.player.current_hp == 0 else self.opponent
