from discord.ext import commands
from models import Character
from models import User
from bot import Bot
import discord


class Adventurer(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.characters = {}

    @commands.command(aliases=['lc', ])
    async def load_char(self, ctx):
        """Query user from database and add to characters if exists"""
        session = self.bot.session
        author_id = ctx.author.id

        character = session.query(Character).filter(User.discord_id == author_id).first()
        await ctx.send(character)
        self.characters[author_id] = character

    @commands.command()
    async def attack(self, ctx):
        pass

    @commands.command()
    async def goto(self, ctx):
        """Go to another place"""
        pass

    @commands.command()
    async def places(self, ctx):
        """Show places"""

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
        author_id = ctx.author.id
        character = self.characters[author_id]

        # Embedded format
        _embed = discord.Embed(
            title=f"{ctx.author.name}'s Profile",
            colour=discord.Colour.orange(),
        )
        _embed.set_thumbnail(url=ctx.author.avatar_url)

        _embed.add_field(
            name='Details',
            value="Level: {}\n"
                  "Exp: {} / {}\n"
                  "Location: {}".format(character.level,
                                        character.exp,
                                        None,
                                        None),
            inline=False
        )
        _embed.add_field(
            name='Stats',
            value="HP: {} / {}\n"
                  "Strength: {}\n"
                  "Defense: {}".format(character.current_hp,
                                       character.max_hp,
                                       character.strength,
                                       character.defense),
            inline=False
        )

        _embed.add_field(
            name='Economy',
            value="Money: {}".format(character.money),
            inline=False
        )

        _embed.set_footer(text='*Simple RPG*', icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=_embed)

    @commands.command()
    async def heal(self, ctx):
        """Uses potion on the character's inventory"""

    @commands.command()
    async def daily(self, ctx):
        """Claim daily rewards, if already claimed show remaining time until next reward"""


def setup(bot):
    bot.add_cog(Adventurer(bot))
