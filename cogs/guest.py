from discord.ext import commands
import models as model
from util import rng


class Guest(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def start(self, ctx: commands.Context):
        """
        display instructions and welcoming message for the guest

        :param ctx:
        """
        pass

    @commands.command()
    async def roll(self, ctx: commands.Context):
        """
        Rolls a die for the guest

        :param ctx: context
        """
        pass

    @commands.command()
    async def confirm(self, ctx: commands.Context):
        """
        Registers the guest

        :param ctx: context
        """
        pass

    @confirm.error
    async def confirm_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Can't confirm, please roll the die first!")


def setup(bot):
    bot.add_cog(Guest(bot))
