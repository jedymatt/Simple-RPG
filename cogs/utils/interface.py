import discord
from discord.ext import commands
from char import player as pl


def empty():
    return '\u200b'


def embed_profile(ctx: commands.Context, player: pl.Player):
    author = ctx.author
    embed = discord.Embed(color=discord.Color.orange())
    embed.set_author(name=f"{author.name}'s Profile", icon_url=author.avatar_url)
    embed.set_thumbnail(url=ctx.author.avatar_url)

    value = f'**Level:** {player.level}\n**Exp:** {player.exp_current}/{player.exp_max}'
    embed.add_field(name='ACHIEVEMENT', value=value, inline=False)
    embed.add_field(name='STATS', value=str_stats(player.stats), inline=False)
    embed.add_field(name='EQUIPMENT', value=str_equipment(player.equipment), inline=False)
    embed.set_footer(text='Simple RPG', icon_url=ctx.bot.user.avatar_url)
    return embed


def embed_bag(ctx: commands.Context, player: pl.Player):
    author = ctx.author
    embed = discord.Embed(color=discord.Color.magenta())
    embed.set_author(name=f"{author.display_name}'s bag", icon_url=ctx.author.avatar_url)
    embed.add_field(name='ITEMS', value=str(player.bag), inline=False)
    embed.add_field(name='MONEY', value=str(player.money), inline=False)
    return embed


def embed_stats(player: pl.Player):
    embed = discord.Embed(color=discord.Color.orange())
    embed.add_field(name='STATS', value=str_stats(stats=player.stats), inline=False)
    return embed


def str_stats(stats: pl.Player.stats):
    hp = f':heart: **HP:** {stats["hp_current"]}/{stats["hp_max"]}'
    attack = f':crossed_swords: **Attack:** {stats["attack"]}'
    defense = f':shield: **Defense:** {stats["defense"]}'
    return f'{hp}\n{attack}\n{defense}'


def str_equipment(equipment):
    sword = f'**Sword:** [{equipment["sword"]}]'
    armor = f'**Armor:** [{equipment["armor"]}]'
    return f'{sword}\n{armor}'


def embed_equipment():
    pass


def main():
    pass


if __name__ == '__main':
    main()
