import random

from models import Attribute


def random_dice():
    return random.choices([1, 2, 3, 4, 5, 6],
                          weights=[.07, .23, .40, .20, .09, .01])[0]


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

    hp = random.randint(minimum, maximum)
    strength = random.randint(minimum, maximum)
    defense = random.randint(minimum, maximum)

    return Attribute(current_hp=hp, max_hp=hp, strength=strength, defense=defense)
