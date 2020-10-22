import discord
from discord.ext import commands

class mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def giverole(self, ctx, member: discord.Member = None, role: discord.Role = None):
    	await member.add_roles(role)
    	await ctx.send('Member Was Given Role.')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member = None, role: discord.Role = None):
    	await member.delete_roles(role)
    	await ctx.send('Member Lost Role.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"I have deleted {amount} messages.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.send(f"You were kicked from {ctx.guild} for : {reason}")
        await member.kick(reason=reason)
        embed=discord.Embed(title=f"{member} Was Kicked✅", color=0x3729ff)
        await ctx.send(embed=embed)

        channel = discord.utils.get(member.guild.channels, name='mod-logs')


        if channel == None:
            return
        else:
            embed=discord.Embed(title=f"Kick Logs", description=f"Author:\n ```{ctx.author}``` Member:\n ```{member}``` Reason:\n```{reason}```")
            await channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.send(f"You were banned from {ctx.guild} for : {reason}")
        await member.ban(reason=reason)
        embed=discord.Embed(title=f"{member} Was Banned✅", color=0x3729ff)
        await ctx.send(embed=embed)

        channel = discord.utils.get(member.guild.channels, name='mod-logs')

        if channel == None:
            return
        else:
            embed=discord.Embed(title=f"Ban Logs", description=f"Author:\n ```{ctx.author}``` Member:\n ```{member}``` Reason:\n```{reason}```")
            await channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = None):

        muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)

        if not muted_role:
            return await ctx.send("You need to make a role called Muted and give it the correct permissions you want.")

        else:
            await member.add_roles(muted_role)
            await member.send(f"You were muted in {ctx.guild} for : {reason}")
            embed=discord.Embed(title=f"{member} Was Muted✅", color=0x3729ff)
            await ctx.send(embed=embed)

        channel = discord.utils.get(member.guild.channels, name='mod-logs')


        if channel == None:
            return
        else:
            embed=discord.Embed(title=f"Mute Logs", description=f"Author:\n ```{ctx.author}``` Member:\n ```{member}``` Reason:\n```{reason}```")
            await channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = None):

        muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)

        if not muted_role:
            return await ctx.send("You need to make a role called Muted and give it the correct permissions you want.")

        else:
            await member.remove_roles(muted_role)
            embed=discord.Embed(title=f"{member} Was Unmuted✅", color=0x3729ff)
            await ctx.send(embed=embed)

        channel = discord.utils.get(member.guild.channels, name='mod-logs')


        if channel == None:
            return
        else:
            embed=discord.Embed(title=f"Mute Logs", description=f"Author:\n ```{ctx.author}``` Member:\n ```{member}``` Reason:\n```{reason}```")
            await channel.send(embed=embed)


    @commands.command()
    async def warn(self, ctx, member : discord.Member, reason):

        if member == None:
            await ctx.send("you need to specify a member")
        else:
            await ctx.send(f"Warned {member} for : {reason}")
            await member.send(f"You have been warned in {ctx.guild} for : {reason}")


            channel = discord.utils.get(member.guild.channels, name='mod-logs')


        if channel == None:
            return
        else:
            embed=discord.Embed(title=f"Warn Logs", description=f"Author:\n ```{ctx.author}``` Member:\n ```{member}``` Reason:\n```{reason}```")
            await channel.send(embed=embed)


def setup(client):
    client.add_cog(mod(client))
