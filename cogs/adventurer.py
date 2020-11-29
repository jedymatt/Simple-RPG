from discord.ext import commands


class Adventurer(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def command(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Adventurer(bot))
