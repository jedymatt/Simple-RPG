from discord.ext import commands
from disbotrpg import Item, ItemPlan, PlanMaterial, Equipment, ShopItem, PlayerItem, Player, User
from db import session
import discord
from cogs.utils.errors import ItemNotFound, InvalidAmount, InsufficientAmount, InsufficientItem
from cogs.utils.stripper import strip_name_amount


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
        author_id = ctx.author.id

        # search for matched plan in plans
        # item_plan = next((item_plan for item_plan in self.item_plans if name.lower() == item_plan.name.lower()), None)
        # if item_plan not exists, then raise an error otherwise proceed

        try:
            # search for matched plan in plans
            item_plan = next(item_plan for item_plan in self.item_plans if name.lower() == item_plan.name.lower())
        except StopIteration:
            raise ItemNotFound('Item not found')

        player = session.query(Player).filter(User.discord_id == author_id).one()

        new_amounts = {}
        success = True
        lack_materials = []
        for material in item_plan.materials:
            # total amount of material
            material_amount = material.amount * amount
            # get player_item that matches material
            player_item: PlayerItem = next(
                (player_item for player_item in player.items if material.item == player_item.item), None)

            if player_item:
                if player_item.amount < material_amount:
                    success = False  # raise an error or count how much is lacking
                    lack_materials.append({'item': player_item.name,
                                           'lack': player_item.amount - material_amount
                                           })
                else:
                    new_amounts[material.item.name] = player_item.amount - material_amount

            else:
                success = False  # no matched player_item in the plan_materials
                lack_materials.append({'item': material.item.name,
                                       'lack': - material_amount
                                       })

        if success:  # if success, overwrite amounts

            for player_item in player.items:
                if player_item.item.name in new_amounts:
                    player_item.amount = new_amounts[player_item.item.name]

            if item_plan.item not in player.items:
                new_player_item = PlayerItem(item=item_plan.item, amount=amount)
                player.items.append(new_player_item)
            else:
                item = next(item for item in player.items if item == item_plan.item)
                item.amount += amount

            await ctx.send('success')

        else:
            embed = discord.Embed(
                title='Craft failed',
                colour=discord.Colour.dark_red()
            )

            msg = '\n'.join(f"{lack['lack']} {lack['item']}" for lack in lack_materials)

            embed.add_field(
                name='Missing materials',
                value=msg
            )

            await ctx.send(embed=embed)

    @craft.error
    async def craft_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the item:')
            await self.craftable(ctx)
        if isinstance(error, ItemNotFound):
            await ctx.send('Invalid item')


def setup(bot):
    bot.add_cog(ItemCommand(bot))
