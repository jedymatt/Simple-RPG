from discord.ext import commands
from models import Character, User, Location
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

    @commands.Cog.listener()
    async def on_ready(self):
        # query locations
        self.locations = session.query(Location).all()

        print('Locations loaded:', end=' ')
        print([location.name for location in self.locations])

    @commands.command()
    async def attack(self, ctx):
        pass

    @commands.command()
    async def goto(self, ctx, arg):
        """Go to another place"""
        pass

    @commands.command()
    async def craft(self, arg):
        pass

    @commands.command(aliases=['loc', 'location', 'locations', 'place'])
    async def places(self, ctx: commands.Context):
        """Show places"""
        embed = discord.Embed(
            title='Places',

            colour=discord.Colour.purple()
        )

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        # _embed.set_thumbnail(url= map thumbnail)

        embed.add_field(
            name="Current Location",
            value='# TODO: get character\'s location',
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

        if user_id not in self.characters:
            self.characters[user_id] = query_character(user_id)

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


def setup(bot):
    bot.add_cog(Adventurer(bot))
