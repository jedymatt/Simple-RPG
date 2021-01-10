from discord.ext import commands
from disbotrpg import Item, ItemPlan, PlanMaterial, Equipment, ShopItem
from db import session
import discord


class ItemCommand(commands.Cog, name='Manage Items Commands'):

    def __init__(self, bot):
        self.bot = bot
        self.plans = session.query(ItemPlan).all()
        self.shop = session.query(ShopItem).all()

    @commands.command(aliases=['craftables', 'plans', 'plan'])
    async def craftable(self, ctx: commands.Context):
        """Show list of craftable items"""

        embed = discord.Embed(
            title='Craftable Items with Materials',
            colour=discord.Colour.purple()
        )

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        for plan in self.plans:
            msg = '\n'.join([f"{mat.amount} {mat.item.name}" for mat in plan.materials])

            embed.add_field(
                name=plan.target_item.name,
                value=msg
            )

        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(ItemCommand(bot))
