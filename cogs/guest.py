from discord.ext import commands
from models import Character
from models import User
from util import rng


class Guest(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.users = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message):
            await message.channel.send("bot mentioned")

        await self.bot.process_commands(message)

    @commands.command()
    async def register(self, ctx: commands.Context):
        """Show register message

        Args:
            ctx:
        """
        print('register command')

    @commands.command()
    async def roll(self, ctx: commands.Context):
        """

        Args:
            ctx:
        """
        pass

    @commands.command()
    async def confirm(self, ctx: commands.Context):
        """

        Args:
            ctx:
        """
        pass

    @confirm.error
    async def confirm_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Can't confirm, please roll the die first!")


def setup(bot):
    bot.add_cog(Guest(bot))
