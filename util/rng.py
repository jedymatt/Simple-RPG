import random as random


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


def random_attribute(die_number) -> tuple:
    if die_number == 1:
        return random.randint(5, 9), random.randint(5, 9), random.randint(5, 9)
    elif die_number == 2:
        return random.randint(10, 14), random.randint(10, 14), random.randint(10, 14)
    elif die_number == 3:
        return random.randint(15, 19), random.randint(15, 19), random.randint(15, 19)
    elif die_number == 4:
        return random.randint(20, 25), random.randint(20, 25), random.randint(20, 25)
    elif die_number == 5:
        return random.randint(26, 40), random.randint(26, 40), random.randint(26, 40)
    elif die_number == 6:
        return 50, 50, 50
    else:
        raise ValueError('Dice number should not exceed 6 or lower than 1')
