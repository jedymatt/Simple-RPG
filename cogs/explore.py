import datetime

import discord
from discord.ext import commands

import models as model
from db import session


class Explore(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def goto(self, ctx, location):
    #     """Go to the specific location"""
    #     pass

    @commands.command()
    async def explore(self, ctx):
        """Explore the location"""
        pass

    @commands.command(aliases=['places'])
    async def locations(self, ctx):
        locations = session.query(model.Location).all()
        embed = discord.Embed(
            title='Locations',
            colour=discord.Colour.dark_green(),
            timestamp=datetime.datetime.now()
        )

        for location in locations:
            embed.add_field(
                name=location.name,
                value=location.description if location.description else '*No Description yet*'
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def gather(self, ctx):
        """Gather raw materials, sometimes failed, sometimes encounter mobs"""
        pass


def setup(bot: commands.Bot):
    bot.add_cog(Explore(bot))
