from discord.ext import commands
from models import Character, User, Location, ItemPlan, CharacterItem
from db import session
import discord
from cogs.utils.errors import CharacterNotFound


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

    result = session.query(Character).filter(User.discord_id == user_id).first()

    if result is None:
        raise CharacterNotFound('Character not found in the database.')

    return result


class Adventurer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.characters = {}
        self.locations = None
        self.item_plans = None

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

        for item_plan in self.item_plans:
            item_plan_name = str(item_plan.item.name).lower()

            if item == item_plan_name:  # check if item is in the item plan

                mats = {}  # create dictionary for the materials
                for mat in item_plan.materials:
                    mats[mat.item.name] = mat.amount

                char_items = {}  # create dictionary for the character items
                for c_item in character.items:
                    char_items[c_item.item.name] = c_item.amount

                # check the items of the character has the mats
                if all(key in char_items for key in mats.keys()):
                    for name in mats:
                        char_amount = char_items.get(name)

                        if char_amount < mats[name]:  # check if character item amount is less than the required amount
                            raise ValueError('Required amount is not enough')  # ValueError is temporary

                        # deduct amount from the required amount
                        char_items[name] -= mats[name]

                    # after traversing the mats, insert remaining amounts of the character's item
                    while char_items:  # char_items is not empty
                        for origin in character.items:
                            origin_name = origin.item.name
                            if origin_name in char_items:
                                origin.amount = char_items[origin_name]
                                del char_items[origin_name]

                    item_exists = False
                    index = 0
                    for index, c_item in enumerate(character.items):
                        if item_plan.item.name == c_item.item.name:
                            item_exists = True
                            break

                    if not item_exists:
                        character.items.append(CharacterItem(item=item_plan.item, amount=1))
                    else:
                        character.items[index].amount += 1

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

    @commands.command()
    async def buy(self, ctx, *, item_name: str):
        pass

    @buy.error
    async def buy_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.shop(ctx)


def setup(bot):
    bot.add_cog(Adventurer(bot))
