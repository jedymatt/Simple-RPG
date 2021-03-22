import datetime
import random

import discord
from discord.ext import commands
from sqlalchemy.sql import func

import models as model
from db import session
from models import util


class Exploration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def goto(self, ctx, location: str):
        """Go to the specific location"""
        author_id = ctx.author.id

        location: model.Location = session.query(model.Location).filter(
            func.lower(model.Location.name) == location.lower()).one()

        player: model.Player = session.query(model.Player).filter(model.User.discord_id == author_id).one()

        if player.level >= location.unlock_level:
            player.location = location
        else:
            raise ValueError('Location is not yet unlocked.')

        await ctx.send('success')

    @commands.command()
    async def explore(self, ctx):
        """Explore the location"""
        pass

    @commands.command(aliases=['places'])
    async def locations(self, ctx):
        locations = session.query(model.Location).all()
        embed = discord.Embed(
            title='Locations',
            colour=discord.Colour.dark_green(),
            timestamp=datetime.datetime.now()
        )

        for location in locations:
            embed.add_field(
                name=location.name,
                value=location.description if location.description else '*No description yet*'
            )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def gather(self, ctx):
        """Gather raw materials, sometimes failed, sometimes encounter mobs"""
        author_id = ctx.author.id
        player: model.Player = session.query(model.Player).filter(model.User.discord_id == author_id).one()

        gathered = []
        location: model.Location = player.location
        for raw_material in location.raw_materials:

            success = util.random_boolean(raw_material.drop_chance)

            if success:
                drop_min = raw_material.drop_amount_min
                drop_max = raw_material.drop_amount_max
                gathered.append((raw_material.raw_material, random.randint(drop_min, drop_max)))

        # declare embed
        embed = discord.Embed(
            title='Gathered',
            colour=discord.Colour.green()
        )

        for gather in gathered:
            # get player_item if none found then value is None
            player_item = next(
                (player_item for player_item in player.items if player_item.item == gather[0]),
                None
            )

            # add item to Player.items
            if player_item:
                player_item.amount += gather[1]
            else:
                # if none, create obj and append it to the Player.items
                player.items.append(
                    model.PlayerItem(
                        item=gather[0],
                        amount=gather[1]
                    )
                )

            # add embed field
            embed.add_field(
                name=gather[0].name,
                value="+%s" % gather[1]
            )

        await ctx.send(str(gathered))

    @gather.error
    async def gather_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error.args)
        else:
            raise error


def setup(bot: commands.Bot):
    bot.add_cog(Exploration(bot))
