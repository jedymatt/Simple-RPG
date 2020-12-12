from discord.ext import commands
from models import Character
from models import User
import discord
from util import rng


class Guest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.users = {}

    @commands.command()
    async def welcome(self, ctx: commands.Context):
        """Shows welcoming message to new players"""
        embed = discord.Embed(
            title='Welcome to Simple-RPG',
            color=discord.Color.dark_gold()
        )
        embed.add_field(name='To get started:', value=f'Type `{self.bot.command_prefix}roll` to roll the die.')
        await ctx.send(embed=embed)

    # @commands.command()
    # async def register(self, ctx: commands.Context):
    #     """Show register message
    #
    #     Args:
    #         ctx:
    #     """
    #
    #     print('register command')

    @commands.command()
    async def roll(self, ctx: commands.Context):
        """

        Args:
            ctx:
        """
        result = rng.die()
        self.users[ctx.author.id] = User(discord_id=ctx.author.id, init_roll=result)
        await ctx.send(result)

    @commands.command()
    async def confirm(self, ctx: commands.Context):
        """

        Args:
            ctx:
        """
        pass

    @confirm.error
    async def confirm_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Can't confirm, please roll the die first!")


def setup(bot):
    bot.add_cog(Guest(bot))
