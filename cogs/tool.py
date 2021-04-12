from discord.ext import commands

from db import session
from models import Player, User


class Tool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_current_hp(self, ctx, new_hp: int):
        player = session.query(Player).filter(User.discord_id == ctx.author.id).one()

        player.current_hp = new_hp
        await ctx.send('done')

    @commands.command()
    async def set_max_hp(self, ctx, new_hp: int):
        player: Player = session.query(Player).filter(User.discord_id == ctx.author.id).one()

        player.max_hp = new_hp

        await ctx.send('done')


def setup(bot):
    bot.add_cog(Tool(bot))
