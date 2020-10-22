import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import json
import aiohttp
from aiohttp import request
import requests
import os
import random
import pymongo
from pymongo import MongoClient

cluster = MongoClient(os.getenv("MONGOPASS"))
db = cluster[os.getenv("MONGO_CLUSTER_NAME')]
collection = db[os.getenv("MONGO_COLLECTION_NAME")]

def get_prefix(client, message):
   results = collection.find({"_id": str(message.guild.id)})
   for result in results:
      return str(result["prefix"])

client = commands.Bot(command_prefix = get_prefix)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('o!help | v0.2.2'))
    print('Online!')

@client.event
async def on_guild_join(guild):
	collection.insert_one({"_id": str(guild.id), "prefix": "o!"})


@client.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, prefix):
   collection.delete_one({"_id": str(ctx.guild.id)})
   collection.insert_one({"_id": str(ctx.guild.id), "prefix": prefix})
   await ctx.send(f'Changed prefix to : {prefix}')

@client.group(invoke_without_command = True)
async def help(ctx):
   embed = discord.Embed(title="Commands", description="[Support Server](https://discord.gg/QNM4CsA) | [Invite](https://discord.com/oauth2/authorize?client_id=738081779050872943&scope=client&permissions=8)")
   embed.add_field(name="😎Fun", value="``help fun`` ", inline=False)
   embed.add_field(name="✨Moderation", value="``help moderation``", inline=False)
   embed.add_field(name="🖼Images", value="``help images``", inline=False)
   embed.add_field(name="🤔Other", value="``help other`` ", inline=False)
   embed.add_field(name="⚒Config", value="``help config`` ", inline=False)
   embed.add_field(name="🎵Music", value="``help music`` ", inline=False)
   embed.add_field(name="💵Economy", value="``help economy`` ", inline=False)
   embed.add_field(name="🥽Server Log", value="``help logging`` ", inline=False)
   await ctx.send(embed=embed)

@help.command(name="moderation")
async def help_moderation(ctx):
 await ctx.send('```asciidoc\nBan :: Bans the mentioned user. usage = ban @user \nKick :: Kicks the mentioned user. usage = kick @user\nPurge :: Deletes messages in bulk. usage = purge <amount of messages>\nGiverole :: Gives the mentioned user a role. usage = giverole @user @role\nMute :: mutes the mentioned user | warning : You Can Not Mute For A Certain Amount Of Time\nUnmute :: unmutes the mentioned user\nWarn :: warns the mentioned user```')

@help.command(name="images")
async def help_images(ctx):
 await ctx.send("```asciidoc\nDog :: Shows you a cute picture of a dog. \nCat :: Shows you a cute picture of a cat.\nMeme :: Generates a random meme from r/dankmemes\n```")

@help.command(name="other")
async def help_other(ctx):
      await ctx.send("```asciidoc\nPing :: shows you the latency of the client.\nHelp :: shows you a help menu.```")

@help.command(name="fun")
async def help_fun(ctx):
      await ctx.send("```asciidoc\nPokedex :: shows you info on any pokemon. usage = pokedex <pokemon>\nRate :: rates what you desire. usage = rate <any word>\nPassword :: sends a random password in your dms\nReverse :: pu uoy evig annog reveN\nF :: pay respects\nSlot :: roll the slot machine \nCoinflip :: Heads!\nCoffee :: drink a cup of coffee with someone (or yourself) usage = coffee @user/coffee\n8ball :: ask the magic 8ball. usage = 8ball <question>\n```")

@help.command(name="music")
async def help_music(ctx):
      await ctx.send("```asciidoc\nJoin :: Joins a voice channel.\nLeave ::   Clears the queue and leaves the voice channel.\nLoop :: Loops the currently playing song.\nNow :: Displays the currently playing song.\nPause ::  Pauses the currently playing song.\nPlay  ::  Plays a song.\nQueue  :: Shows the player's queue.\nRemove :: Removes a song from the queue at a given index.\nResume :: Resumes a currently paused song.\nShuffle :: Shuffles the queue. \nSkip :: Vote to skip a song. The requester can automatically skip.\nStop :: Stops playing song and clears the queue.\nSummon :: Summons the bot to a voice channel.\nVolume :: Sets the volume of the player.\n```")

@help.command(name="economy")
async def help_economy(ctx):
 await ctx.send("```asciidoc\nBalance :: Shows you the amount of $$$$ you have.\nDeposit/Withdraw :: Deposits or withdraws the selected amount of money\nLeaderboard :: shows you the richest people on the entire bot\nShop :: Buy some stuff with your $$$\nSell :: sell back something if you dont like it.\nBuy :: buy the stuff you see in the shop\nGive :: give someone money\nBeg :: ask for money on the street\nBag :: see what you have bought\n```")

@help.command(name="config")
async def help_config(ctx):
 await ctx.send("Only config command is 'prefix'.")

@help.command(name="logging")
async def help_logging(ctx):
 await ctx.send("```asciidoc\nMessagelog :: Creates a channel called \"msg-logs\" and logs whenever a message is deleted or edited\n\nModlog :: Creates a channel called \"mod-logs\" and logs whenever a mod mutes/bans/warns/kicks a person using this bot.\n```")

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! it took ``{round(client.latency * 100)}``ms for the bot to respond')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
       client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_message_delete(message):
  channel = discord.utils.get(message.guild.channels, name='msg-logs')
  embed = discord.Embed(title=f'Message deleted in #{message.channel.name}\n----------------------------------------', color = discord.Color(0xfa43ee))
  embed.add_field(name='Message author', value=f'{message.author}', inline=False)
  embed.add_field(name='Message', value=f'{message.content}', inline=False)
  await channel.send(embed=embed)

@client.event
async def on_message_edit(before, after):
  channel = discord.utils.get(before.guild.channels, name='msg-logs')
  embed = discord.Embed(title=f'Message edited in #{before.channel.name}\n----------------------------------------', color = discord.Color(0xfa43ee))
  embed.add_field(name='Message author:', value=f'{before.author}', inline=False)
  embed.add_field(name='Before:', value=f'{before.content}', inline=False)
  embed.add_field(name='After:', value=f'{after.content}', inline=False)
  await channel.send(embed=embed)

@commands.has_permissions(administrator=True)
@client.command()
async def messagelog(ctx):
  await ctx.guild.create_text_channel(name='msg-logs')
  await ctx.send("Done!")

@commands.has_permissions(administrator=True)
@client.command()
async def modlog(ctx):
  await ctx.guild.create_text_channel(name='mod-logs')
  await ctx.send("Done!")

@commands.is_owner()
@client.command()
async def playing(ctx, game):
   await client.change_presence(activity=discord.Game(name=game))
   await ctx.send('ok')

@client.event
async def on_error(ctx, error):
  if isinstance(error, discord.ext.commands.CommandNotFound):
      return
  elif isinstance(error, discord.ext.commands.CommandOnCooldown):
      await ctx.send(f"You are on a cooldown. try again in ``{error.retry_after:,.2f}``s.")
  elif isinstance(error, AttributeError):
      return
  elif isinstance(error, TypeError):
      return
  else:
      embed=discord.Embed(title="❌ERROR", description=f"```{str(error)}```")
      await ctx.send(embed=embed)

client.run(os.getenv("TOKEN"))
