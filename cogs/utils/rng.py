import random
from models import Attribute


def die():
    percentage = random.randint(1, 100)
    if percentage == 100:  # 1%
        return 6
    elif percentage > 90:  # 9%
        return 5
    elif percentage > 70:  # 20%
        return 4
    elif percentage > 30:  # 40%
        return 3
    elif percentage > 7:  # 23%
        return 2
    else:  # 7%
        return 1


def random_attribute(die_number) -> Attribute:
    # minimum, maximum = 0, 0
    if die_number == 1:
        minimum, maximum = 5, 9
    elif die_number == 2:
        minimum, maximum = 10, 14
    elif die_number == 3:
        minimum, maximum = 15, 19
    elif die_number == 4:
        minimum, maximum = 20, 25
    elif die_number == 5:
        minimum, maximum = 26, 40
    elif die_number == 6:
        minimum, maximum = 50, 50
    else:
        raise ValueError('Dice number should not exceed 6 or lower than 1')

    hp = random.randint(minimum, maximum) + 50
    strength = random.randint(minimum, maximum) + 15
    defense = random.randint(minimum, maximum) + 5

    return Attribute(hp=hp, strength=strength, defense=defense)
