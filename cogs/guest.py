from discord.ext import commands
from models import Character, User
from util import rng


class Guest(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client
        self.users = {}

    @commands.command()
    async def register(self, ctx: commands.Context):
        """
        display instructions and welcoming message for the guest

        :param ctx:
        """
        self.users[ctx.author.id] = User(discord_id=ctx.author.id)
        await ctx.send('{} is now registered'.format(ctx.author))

    @commands.command()
    async def roll(self, ctx: commands.Context):
        """
        Rolls a die for the guest

        :param ctx: context
        """
        roll_result = rng.die()
        self.users[ctx.author.id].init_roll = roll_result
        print(self.users[ctx.author.id])
        await ctx.send(roll_result)

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
