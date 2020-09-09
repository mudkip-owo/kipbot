import discord
from discord.ext import commands
import json
import aiohttp
from aiohttp import request
import requests
import random

class nsfw(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_nsfw()
    async def porn(self, ctx):
      url = 'https://meme-api.herokuapp.com/gimme/porn'
      result_url = requests.get(url)
      resultjson=result_url.json()
      await ctx.send(resultjson['url'])

    @commands.command()
    @commands.is_nsfw()
    async def porngif(self, ctx):
      url = 'https://meme-api.herokuapp.com/gimme/porngifs'
      result_url = requests.get(url)
      resultjson=result_url.json()
      await ctx.send(resultjson['url'])

    @commands.command()
    @commands.is_nsfw()
    async def hentai(self, ctx):
      url = 'https://meme-api.herokuapp.com/gimme/hentai'
      result_url = requests.get(url)
      resultjson=result_url.json()
      await ctx.send(resultjson['url'])

def setup(client):
    client.add_cog(nsfw(client))
