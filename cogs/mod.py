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
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name , member_dscriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_dscriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'User was unbanned')
                return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send('User was banned')


def setup(client):
    client.add_cog(mod(client))
