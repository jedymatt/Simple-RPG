from discord.ext import commands
from disbotrpg import Item, ItemPlan, PlanMaterial, Equipment, ShopItem, PlayerItem
from db import session
import discord
from cogs.utils.errors import ItemNotFound, InvalidAmount, InsufficientAmount, InsufficientItem


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

    @commands.command()
    async def craft(self, ctx, *, arg: str):
        item = arg.lower()
        author_id = ctx.author.id

        player = query_player(author_id)

        item_plan: ItemPlan = get_item(item, self.item_plans)

        if item_plan:

            plan_mats = {}  # create dictionary for the materials
            for mat in item_plan.materials:
                plan_mats[mat.name] = mat.amount

            char_items = {}  # create dictionary for the player items
            for c_item in player.items:
                char_items[c_item.name] = c_item.amount

            if all(key in char_items for key in plan_mats.keys()):
                for name in plan_mats:
                    char_amount = char_items[name]

                    if char_amount < plan_mats[name]:  # check if player item amount is less than the required amount
                        raise InsufficientAmount('Required amount is not enough')

                    # deduct amount from the required amount
                    char_items[name] -= plan_mats[name]

                # after traversing the mats, copy remaining amounts of char_items to the player.items
                while char_items:  # char_items is not empty
                    for c_item in player.items:
                        name = c_item.name
                        if name in char_items:
                            c_item.amount = char_items[name]
                            del char_items[name]

                item = get_item(item_plan.item.name, player.items)
                if item:
                    item.amount += 1
                else:
                    player.items.append(PlayerItem(item=item_plan.item, amount=1))

            else:
                raise InsufficientItem('not enough materials')
        else:
            raise ItemNotFound('invalid item')

        session.commit()


def setup(bot):
    bot.add_cog(ItemCommand(bot))
