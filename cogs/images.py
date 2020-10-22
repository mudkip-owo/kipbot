import discord
from discord.ext import commands
import json
import aiohttp
from aiohttp import request
import requests
import random

class images(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def dog(self,ctx):
      url = 'https://some-random-api.ml/img/dog'
      result_url = requests.get(url)
      resultjson=result_url.json()
      embed = discord.Embed(title="here is your dog.")
      embed.set_image(url=resultjson['link'])
      await ctx.send(embed=embed)


    @commands.command()
    async def cat(self,ctx):
      url = 'https://some-random-api.ml/img/cat'
      result_url = requests.get(url)
      resultjson=result_url.json()
      embed = discord.Embed(title="here is your cat.")
      embed.set_image(url=resultjson['link'])
      await ctx.send(embed=embed)

    @commands.command()
    async def meme(self,ctx):
      url = 'https://meme-api.herokuapp.com/gimme/dankmemes'
      result_url = requests.get(url)
      resultjson=result_url.json()
      embed = discord.Embed(title=resultjson['title'])
      embed.set_image(url=resultjson['url'])
      await ctx.send(embed=embed)



def setup(client):
    client.add_cog(images(client))
