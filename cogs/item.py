from discord.ext import commands
from disbotrpg import Item, ItemPlan, PlanMaterial, Equipment, ShopItem, PlayerItem, Player, User
from db import session
import discord
from cogs.utils.errors import ItemNotFound, InvalidAmount, InsufficientAmount, InsufficientItem
from cogs.utils.stripper import strip_name_amount


def get_plan(item_name, plans):
    for plan in plans:
        if item_name == str(plan.item.name).lower():
            return plan

    return None


class ItemCommand(commands.Cog, name='Manage Items'):

    def __init__(self, bot):
        self.bot = bot
        self.item_plans = session.query(ItemPlan).all()
        self.shop_items = session.query(ShopItem).all()

    @commands.command(aliases=['craftables', 'plans', 'plan'])
    async def craftable(self, ctx: commands.Context):
        """Show list of craftable items"""

        embed = discord.Embed(
            title='Craftable Items with Materials',
            colour=discord.Colour.purple()
        )

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        for item_plan in self.item_plans:
            msg = '\n'.join([f"{mat.amount} {mat.item.name}" for mat in item_plan.materials])

            embed.add_field(
                name=item_plan.item.name,
                value=msg
            )

        await ctx.send(content=f'**{ctx.author.name}**', embed=embed)

    @commands.command()
    async def craft(self, ctx: commands.Context, *, arg: str):
        name, amount = strip_name_amount(arg)

        pass
        #
        # item_name = arg.lower()
        # author_id = ctx.author.id
        #
        # player: Player = session.query(Player).filter(User.discord_id == author_id).one()
        #
        # # search for matched plan in plans
        # item_plan: ItemPlan = get_plan(item_name, self.item_plans)
        #
        # if item_plan:
        #     # check if player's items are in the materials, and if it
        #
        #     new_amounts = {}
        #     for material in item_plan.materials:
        #
        #         for player_item in player.items:
        #
        #             if player_item.item == material.item:
        #                 if player_item.amount > material.amount:
        #                     break
        #                 else:
        #                     raise InsufficientAmount('Not enough amount')
        #         else:
        #             raise InsufficientItem('Not enough item')
        #
        #         new_amounts[material.item.name] = material.amount - player_item.amount
        #
        #     for player_item in player.items:
        #         if player_item.item.name in new_amounts:
        #             player_item.amount = new_amounts[player_item.item.name]
        #
        #     if item_plan.item not in player.items:
        #         new_item = ItemPlan(item=item_plan.item)
        #         player.items.append(new_item)
        #     else:
        #         for old_item in item

        # plan_mats = {}  # create dictionary for the materials
        # for mat in plan.materials:
        #     plan_mats[mat.name] = mat.amount
        #
        # char_items = {}  # create dictionary for the player items
        # for c_item in player.items:
        #     char_items[c_item.name] = c_item.amount
        #
        # if all(key in char_items for key in plan_mats.keys()):
        #     for name in plan_mats:
        #         char_amount = char_items[name]
        #
        #         if char_amount < plan_mats[name]:  # check if player item amount is less than the required amount
        #             raise InsufficientAmount('Required amount is not enough')
        #
        #         # deduct amount from the required amount
        #         char_items[name] -= plan_mats[name]
        #
        #     # after traversing the mats, copy remaining amounts of char_items to the player.items
        #     while char_items:  # char_items is not empty
        #         for c_item in player.items:
        #             name = c_item.name
        #             if name in char_items:
        #                 c_item.amount = char_items[name]
        #                 del char_items[name]
        #
        #     item_name = get_item(plan.item.name, player.items)
        #     if item_name:
        #         item_name.amount += 1
        #     else:
        #         player.items.append(PlayerItem(item=plan.item, amount=1))
        #
        # else:
        #     raise InsufficientItem('not enough materials')
        # else:
        # raise ItemNotFound('invalid item')

    session.commit()


def setup(bot):
    bot.add_cog(ItemCommand(bot))
