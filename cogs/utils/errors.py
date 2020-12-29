from discord.ext import commands


class NoDieRoll(commands.CheckFailure):
    pass


class CharacterNotFound(commands.CheckFailure):
    pass
