import db
import os

import discord
from discord.ext import commands
from models import User, Character


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = db.engine
        self.session = db.session


def main():
    bot = Bot(command_prefix='.')

    @bot.command()
    async def character(ctx: commands.Context):
        """check if character exists"""
        session = bot.session
        author_id = ctx.author.id

        char = session.query(Character).filter(User.discord_id == author_id).first()
        await ctx.send(char)

    @bot.command()
    async def user(ctx: commands.Context):
        """check if user exists """
        session = bot.session
        author_id = ctx.author.id

        usr = session.query(User).filter(User.discord_id == author_id).first()
        await ctx.send(usr)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')

    @bot.command()
    async def ping(ctx: commands.Context):
        await ctx.send(f'Ping: `{round(bot.latency, 2)}ms`')

    # load cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

    # connect to database
    bot.engine.connect()

    # run bot
    bot.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
