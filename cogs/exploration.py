from discord.ext import commands
import models as model


class Exploration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def goto(self, ctx, location):
    #     """Go to the specific location"""
    #     pass
    #
    # @commands.command()
    # async def explore(self, ctx):
    #     """Explore the location"""
    #     pass
    #
    # @commands.command()
    # async def gather(self, ctx):
    #     """Gather raw materials, sometimes failed, sometimes encounter mobs"""
    #     pass


def setup(bot: commands.Bot):
    bot.add_cog(Exploration(bot))
