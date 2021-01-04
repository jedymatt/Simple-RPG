from discord.ext import commands
from models import Character, User, Location, ItemPlan, CharacterItem, Item
from db import session
import discord
from cogs.utils.errors import CharacterNotFound, InvalidAmount, ItemNotFound, InsufficientAmount, InsufficientItem


def query_character(user_id):
    """
    Finds user's character from database.

    Args:
        user_id: discord user id

    Returns:
        Character: Character that matches the user's id

    Raises:
         CharacterNotFound: If the character is not found in the database
    """

    result = session.query(Character).filter(User.discord_id == user_id).one()

    if result is None:
        raise CharacterNotFound('Character not found in the database.')

    return result


def get_item(item_name: str, items):
    for item in items:
        if item_name.lower() == str(item.name).lower():
            return item

    return None


def split_str_int(arg: str):
    """

    Splits the string into new string and integer.
    Default integer is 1 if not specified.

    Args:
        arg: string with any content followed by integer

    Returns: string and integer
    """
    arg = arg.split(' ')
    size = len(arg)

    integer = arg[size - 1]

    try:
        integer = int(integer)
        string = ' '.join(arg[:size - 1])
    except ValueError:
        integer = 1
        string = ' '.join(arg)

    return string, integer


class Adventurer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.characters = {}
        self.locations = None
        self.item_plans = None
        self.shop_items = None

    @commands.Cog.listener()
    async def on_ready(self):
        # query locations
        self.locations = session.query(Location).all()

        print('Locations loaded:', end=' ')
        print([location.name for location in self.locations])

        self.item_plans = session.query(ItemPlan).all()
        print('Item plans loaded')

        # temporary, load characters
        list_chars = session.query(Character).all()
        for char in list_chars:
            self.characters[char.user.discord_id] = char

        # load shop items
        self.shop_items = session.query(Item).filter(Item.in_shop == 1).order_by(Item.money_value.asc()).all()
        print(self.shop_items)

    @commands.command()
    async def attack(self, ctx):
        pass

    @commands.command()
    async def goto(self, ctx, *, location_name: str):
        """Go to another place"""
        author_id = ctx.author.id
        character = self.characters[author_id]

        location_name = location_name.lower()

        for location in self.locations:
            if location_name == str(location.name).lower():
                character.location = location

    @commands.command(aliases=['plan', 'plans'])
    async def item_plan(self, ctx):
        """Show list of craftable items"""

        embed = discord.Embed(
            title='Craft',
            colour=discord.Colour.purple()
        )

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        for item_plan in self.item_plans:
            str_materials = '\n'.join([f"{mat.amount} {mat.item.name}" for mat in item_plan.materials])

            embed.add_field(
                name=item_plan.item.name,
                value=str_materials,
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def craft(self, ctx, *, arg: str):
        item = arg.lower()
        author_id = ctx.author.id

        character = self.characters[author_id]

        item_plan: ItemPlan = get_item(item, self.item_plans)

        if item_plan:

            plan_mats = {}  # create dictionary for the materials
            for mat in item_plan.materials:
                plan_mats[mat.name] = mat.amount

            char_items = {}  # create dictionary for the character items
            for c_item in character.items:
                char_items[c_item.name] = c_item.amount

            if all(key in char_items for key in plan_mats.keys()):
                for name in plan_mats:
                    char_amount = char_items[name]

                    if char_amount < plan_mats[name]:  # check if character item amount is less than the required amount
                        raise InsufficientAmount('Required amount is not enough')

                    # deduct amount from the required amount
                    char_items[name] -= plan_mats[name]

                # after traversing the mats, copy remaining amounts of char_items to the character.items
                while char_items:  # char_items is not empty
                    for c_item in character.items:
                        name = c_item.item.name
                        if name in char_items:
                            c_item.amount = char_items[name]
                            del char_items[name]

                item = get_item(item_plan.name, character.items)
                if item:
                    item.amount += 1
                else:
                    character.items.append(CharacterItem(item=item_plan.item, amount=1))

            else:
                raise InsufficientItem('not enough materials')
        else:
            raise ItemNotFound('invalid item')

    @commands.command(aliases=['loc', 'location', 'locations', 'place'])
    async def places(self, ctx: commands.Context):
        """Show places"""
        embed = discord.Embed(
            title='Places',

            colour=discord.Colour.purple()
        )

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        # _embed.set_thumbnail(url= map thumbnail)

        char = self.characters[ctx.author.id]

        embed.add_field(
            name="Current Location",
            value=str(char.location.name if char.location else 'None'),
            inline=False
        )

        str_loc = '\n'.join([f"{location.name} - *{location.description}*" for location in self.locations])

        embed.add_field(
            name='All Places',
            value=str_loc
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def gather(self, ctx):
        """Gather raw materials"""
        pass

    @commands.command()
    async def explore(self, ctx):
        """Explore the current area"""

    @commands.command()
    async def profile(self, ctx: commands.Context):
        """Show profile"""
        user_id = ctx.author.id

        # if user_id not in self.characters:
        #     self.characters[user_id] = query_character(user_id)

        character = self.characters[user_id]

        # Embedded format
        embed = discord.Embed(
            title=f"{ctx.author.name}'s profile",
            colour=discord.Colour.orange(),
        )

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        # _embed.set_thumbnail(url= avatar logo)

        embed.add_field(
            name='Details',
            value="Level: {}\n"
                  "Exp: {} / {}\n"
                  "Location: {}".format(character.level,
                                        character.exp,
                                        character.next_level_exp(),
                                        character.location.name if character.location else None
                                        ),
            inline=False
        )
        embed.add_field(
            name='Stats',
            value="HP: {} / {}\n"
                  "Strength: {}\n"
                  "Defense: {}".format(character.current_hp,
                                       character.max_hp,
                                       character.strength,
                                       character.defense),
            inline=False
        )

        embed.add_field(
            name='Others',
            value="Money: {}".format(character.money),
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def heal(self, ctx):
        """Uses potion on the character's inventory"""

    @commands.command()
    async def daily(self, ctx):
        """Claim daily rewards, if already claimed show remaining time until next reward"""

    @commands.command()
    async def items(self, ctx):
        """Show list of items"""
        author_id = ctx.author.id

        character = self.characters[author_id]

        string_items = '\n'.join([f"{char_item.amount} {char_item.item.name}" for char_item in character.items])

        await ctx.send(string_items)

    @commands.command()
    async def shop(self, ctx):
        """Shows list of items in the shop"""
        shop_items_string = '\n'.join([f"{item.name} cost:{item.money_value}" for item in self.shop_items])

        await ctx.send(shop_items_string)

    @commands.command()
    async def buy(self, ctx, *, item_name_amount: str):

        item_name, item_amount = split_str_int(item_name_amount)

        # if amount is not valid throw an error
        if item_amount <= 0:
            raise InvalidAmount('Amount reached zero or below zero.')

        # get user's character
        character = self.characters[ctx.author.id]

        shop_item = get_item(item_name, self.shop_items)

        if shop_item:
            total_cost = shop_item.money_value * item_amount

            # check if money is enough before making transaction
            if total_cost > character.money:
                raise ValueError(f"Not enough money to buy '{item_name}'")

            # Deduct money
            character.money -= total_cost

            # check if item to be added is already in the character.items otherwise create object
            item = get_item(item_name, character.items)
            if item:
                item.amount += item_amount
            else:
                character.items.append(CharacterItem(item=shop_item, amount=item_amount))
        else:
            raise ItemNotFound

        await ctx.send('item added to inventory, new balance: {}'.format(character.money))

    @buy.error
    async def buy_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.shop(ctx)

        if isinstance(error, InvalidAmount):
            await ctx.send('invalid amount')

        if isinstance(error, ItemNotFound):
            await ctx.send('invalid item')

    @commands.command()
    async def sell(self, ctx, *, item_name_amount: str):
        pass


def setup(bot):
    bot.add_cog(Adventurer(bot))
