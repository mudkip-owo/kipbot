import random
import discord
import urllib
import secrets
import asyncio
import aiohttp
import re
from io import BytesIO
from discord.ext import commands
import json


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails']
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Pay your respects """
        hearts = ['❤', '💛', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")


    @commands.command(aliases=["8ball", "eightball"])
    async def _8ball(self, ctx, *, question):
        responses = ["🎱It is certain.",
                     "🎱It is decidedly so.",
                     "🎱Without a doubt.",
                     "🎱Yes - definitely.",
                     "🎱You may rely on it.",
                     "🎱As I see it, yes.",
                     "🎱Most likely.",
                     "🎱Outlook good.",
                     "🎱Yes.",
                     "🎱Signs point to yes.",
                     "🎱Reply hazy, try again.",
                     "🎱Ask again later.",
                     "🎱Better not tell you now.",
                     "🎱Cannot predict now.",
                     "🎱Concentrate and ask again.",
                     "🎱Don't count on it.",
                     "🎱My reply is no.",
                     "🎱My sources say no.",
                     "🎱Outlook not so good.",
                     "🎱Very doubtful."]
        await ctx.send(random.choice(responses))



    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """ esreveR """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        embed = discord.Embed(title='Ophelia Reverse!', description=t_rev)
        await ctx.send(embed=embed)

    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        """ Generates a random password string for you in dms """
        if nbytes not in range(3, 1401):
            return await ctx.send("I only accept any numbers between 3-1400")
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
        await ctx.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")

    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        rate_amount = random.uniform(0.0, 100.0)
        await ctx.send(f"I'd rate `{thing}` a **{round(rate_amount, 4)} / 100**")

    @commands.command()
    async def coffee(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Give someone a coffee (or drink it yourself) """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: Drank a cup of coffee☕ ")
        if user.id == self.bot.user.id:
            return await ctx.send("*i drink coffee with you* ☕")
        if user.bot:
            return await ctx.send(f"I would love to give coffee to the bot **{ctx.author.name}**, but I don't think it would respond...")

        coffee_offer = f"**{user.name}**, you got a ☕ offer from **{ctx.author.name}** (react to accept)"
        cofeee_offer = coffe_offer + f"\n\n**Reason:** {reason}" if reason else coffee_offer
        msg = await ctx.send(coffee_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "☕":
                return True
            return False

        try:
            await msg.add_reaction("☕")
            await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely coffee together☕")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{user.name}** wanted a cup of coffee with you **{ctx.author.name}**")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            coffee_offer = f"**{user.name}**, you got a ☕ from **{ctx.author.name}**"
            cofeee_offer = coffee_offer + f"\n\n**Reason:** {reason}" if reason else coffee_offer
            await msg.edit(content=coffee_offer)


    @commands.command(aliases=['slots', 'bet'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll a slot machine """
        emojis = "🟥🟦🟩🟪🟧🟨⬜🟧"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} ALL MATCHING! WIN WIN")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 matching, win!")
        else:
            await ctx.send(f"{slotmachine} none matching, you lost 😢")
    
    @commands.is_owner()
    @commands.command()
    async def addpremium(ctx, member : discord.Member):
    	with open('premiumusers.json', 'w') as f:
    		json.dump(member, f)


def setup(bot):
    bot.add_cog(fun(bot))
