import db
import os

import discord
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = db.engine
        self.session = db.session


def main():
    bot = Bot(command_prefix='.')

    @bot.event
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    @bot.command()
    async def ping(ctx: commands.Context):
        await ctx.send(f'Ping: `{round(bot.latency, 2)}ms`')

    # load cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

    # connect to database
    # bot.engine.connect()

    # run bot
    bot.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
