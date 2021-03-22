from discord.ext import commands

from cogs.utils import rng
from db import session
from models import User, Player
from models.config import BASE_HP, BASE_STRENGTH, BASE_DEFENSE


# TODO: (least priority) add task to commit every 5 minutes or so, check 'confirm' method

class Register(commands.Cog):

    def __init__(self, bot):
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

        result = rng.random_dice()

        if ctx.author.id not in self.users:  # if user is not in dictionary, then create User object
            user = User(discord_id=ctx.author.id, dice_roll=result)
            self.users[ctx.author.id] = user
            session.add(user)
        else:  # else modify the init_roll
            user = self.users[ctx.author.id]
            user.dice_roll = result

        # session.commit()
        await ctx.send(str(user))

    @commands.command()
    async def confirm(self, ctx: commands.Context):
        """ Finalizes the result and start to create character

        Args:
            ctx:
        """
        user = self.users[ctx.author.id]
        player = Player(level=1, exp=0, money=500, stat_growth=1.5)
        player.attribute = rng.random_attribute(user.dice_roll)
        player.attribute.current_hp += BASE_HP
        player.attribute.max_hp += BASE_HP
        player.attribute.strength += BASE_STRENGTH
        player.attribute.defense += BASE_DEFENSE
        user.player = player

        session.commit()

        await ctx.send(str(player))

    # @confirm.error
    # async def confirm_error(self, ctx, error):
    #     if isinstance(error, commands.CheckFailure):
    #         await ctx.send("Can't confirm, please roll the die first!")

    @commands.command()
    async def rollback(self, ctx):
        session.rollback()

        await ctx.send('connection rollback')


def setup(bot):
    bot.add_cog(Register(bot))
