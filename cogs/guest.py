from discord.ext import commands
from models import Character
from models import User
import discord
from util import rng
from bot import Bot


class Register(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.users = {}

    @commands.command()
    async def welcome(self, ctx: commands.Context):
        """Shows welcoming message to new players"""
        # sends welcoming message and intro to the game, and give instruction to roll the die
        await ctx.send("welcoming message and intro to the game, and give instruction to roll the die")

    @commands.command()
    async def roll(self, ctx: commands.Context):
        """

        Args:
            ctx:
        """
        result = rng.die()
        user = User(discord_id=ctx.author.id, init_roll=result)
        self.users[ctx.author.id] = user
        self.bot.session.add(user)
        await ctx.send(str(user))

    @commands.command()
    async def confirm(self, ctx: commands.Context):
        """ Finalizes the result and start to create character

        Args:
            ctx:
        """
        user = self.users[ctx.author.id]
        character = Character(level=1, exp=0, money=500)
        character.attribute = rng.random_attribute(user.init_roll)
        user.character = character

        user.character.current_hp = user.character.max_hp
        self.bot.session.commit()

        await ctx.send(str(character))

    # @confirm.error
    # async def confirm_error(self, ctx, error):
    #     if isinstance(error, commands.CheckFailure):
    #         await ctx.send("Can't confirm, please roll the die first!")


def setup(bot):
    bot.add_cog(Register(bot))
