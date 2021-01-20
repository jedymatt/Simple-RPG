from discord.ext import commands


class Exploration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def setup(bot: commands.Bot):
    bot.add_cog(Exploration(bot))
