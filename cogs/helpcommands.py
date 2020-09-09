import discord
from discord.ext import commands

class helpcommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
     embed=discord.Embed(title="Commands", description="")
     embed.add_field(name="✨Moderation", value="``-help_moderation``", inline=False)
     embed.add_field(name="🔞NSFW", value="``-help_nsfw``", inline=False)
     embed.add_field(name="🖼Images", value="``-help_images``", inline=False)
     embed.add_field(name="🤔Other", value="``-help_other`` ", inline=False)
     embed.add_field(name="😎Fun", value="``-help_fun``     ", inline=False)
     embed.add_field(name="", value="[Support Server](https://discord.gg/QNM4CsA) | [Bot Invite](https://discord.com/oauth2/authorize?client_id=738081779050872943&scope=bot&permissions=8)", inline=False)
     await ctx.send(embed=embed)

    @commands.command()
    async def help_moderation(self, ctx):
     embed=discord.Embed(title="✨Moderation", description="``ban``, ``unban``, ``kick``, ``purge``, ``giverole``.", color=0x5900b3)
     await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def help_nsfw(self, ctx):
     embed=discord.Embed(title="🔞NSFW", description="``porn``, ``porngif``, ``hentai``.", color=0x5900b3)
     await ctx.send(embed=embed)

    @commands.command()
    async def help_images(self, ctx):
     embed=discord.Embed(title="🖼Images", description="``dog``, ``cat``, ``meme``.", color=0x5900b3)
     await ctx.send(embed=embed)

    @commands.command()
    async def help_other(self, ctx):
     embed=discord.Embed(title="🤔Other", description="``ping``,  ``help``.", color=0x5900b3)
     await ctx.send(embed=embed)

    @commands.command()
    async def help_fun(self, ctx):
     embed=discord.Embed(title="😎Fun", description="``pokedex``, ``rate``, ``password``, ``reverse``, ``f``, ``slot``, ``coinflip``, ``howgay``, ``beer``, ``hotcalc``, ``howgay``.", color=0x5900b3)
     await ctx.send(embed=embed)


def setup(client):
    client.add_cog(helpcommands(client))
