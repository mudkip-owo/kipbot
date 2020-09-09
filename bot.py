import discord
import os
from discord.ext import commands
import json

client = commands.Bot(command_prefix = "-")
client.remove_command('help')

@client.event
async def on_ready():
 await client.change_presence(activity = discord.Streaming(name = "-help", url = "https://www.twitch.tv/discord"))
 print("yes")

@client.command()
async def load(ctx, extension):
   client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
   client.unload_extension(f'cogs.{extension}')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! it took ``{round(client.latency * 100)}``ms for the bot to respond')

@client.command()
async def commands(ctx):
    await ctx.send("help\npokedex\nslot\nf\nhotcalc\nhowgay\npurge\nban\nunban\nkick\ncoinflip\nreverse\nrate\nbeer\npassword\ndog\ncat\nmeme\n-help_nsfw :eyes:")

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.errors.NSFWChannelRequired):
     return await ctx.send('You need to use this command in an NSFW channel!')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
       client.load_extension(f'cogs.{filename[:-3]}')

client.run('token')
