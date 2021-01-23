import discord
from discord.ext import commands

from db import session
from models import Player, User


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx: commands.Context):
        """Show profile"""
        user_id = ctx.author.id

        player = session.query(Player).filter(User.discord_id == user_id).one()

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
                  "Location: {}".format(player.level,
                                        player.exp,
                                        player.next_level_exp(),
                                        player.location.name if player.location else None
                                        ),
            inline=False
        )
        embed.add_field(
            name='Stats',
            value="HP: {} / {}\n"
                  "Strength: {}\n"
                  "Defense: {}".format(player.current_hp,
                                       int(player.max_hp),
                                       int(player.strength),
                                       int(player.defense)),
            inline=False
        )

        embed.add_field(
            name='Others',
            value="Money: {}".format(player.money),
            inline=False
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
