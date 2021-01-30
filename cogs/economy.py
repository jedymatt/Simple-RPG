import discord
from discord.ext import commands

import models as model
from cogs.utils import stripper
from db import session


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx):
        shop_items = session.query(model.ShopItem).all()

        embed = discord.Embed(
            title='Items for sale',
            colour=discord.Colour.random()
        )

        for shop_item in shop_items:
            shop_item: model.ShopItem = shop_item

            embed.add_field(
                name="%s coins - **%s**" % (shop_item.item.market_value, shop_item.item.name),
                value=shop_item.item.description if shop_item.item.description else '*No description yet*'
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, *, args):
        name, amount = stripper.strip_name_amount(args)

    async def sell(self, ctx, *, args):
        pass


def setup(bot: commands.Bot):
    bot.add_cog(Economy(bot))
