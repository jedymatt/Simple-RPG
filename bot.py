from config import BOT_TOKEN
from db import engine
import os
import discord
from discord.ext import commands
from disbotrpg import config


def main():
    config.set_hp_regen(10, 600)  # set global variable for Player to regenerate HP

    bot = commands.Bot(command_prefix='.', case_insensitive=True)

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
    engine.connect()

    # run bot
    bot.run(BOT_TOKEN)


if __name__ == '__main__':
    main()
