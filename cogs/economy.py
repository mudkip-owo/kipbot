import discord
from discord.ext import commands
from bot import BucketType

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client


cluster = MongoClient(os.getenv("MONGOPASS"))
db = cluster[os.getenv("MONGO_CLUSTER_NAME')]
collection = db[os.getenv("MONGO_COLLECTION_NAME")]

	@commands.cooldown(1, 3, commands.BucketType.user)
	@commands.command(aliases=['bal'])
	async def balance(self, ctx, member: discord.Member=none):
	  findbal=collection.find_one({"_id": str(ctx.author.id)})
	  if not findbal:
	    collection.insert_one({"_id": str(ctx.author.id), "wallet": 0, "bank": 0})
	    embed=discord.Embed(title=f'{ctx.author.name}\'s balance')
	    embed.add_field(name='**Wallet:**',value='0', inline=False)
	    embed.add_field(name='**Bank:**',value='0', inline=False)
	    await ctx.send(embed=embed)
	  else:
	    embed=discord.Embed(title=f'{ctx.author.name}\'s balance')
	    embed.add_field(name='**Wallet:**',value=findbal['wallet'], inline=False)    
	    embed.add_field(name='**Bank:**',value=findbal['bank'], inline=False)
	    await ctx.send(embed=embed)

	@commands.cooldown(1, 2, commands.BucketType.user)
	@commands.command(aliases=['dep'])
	async def deposit(self, ctx, amount : int):
	  findbal = collection.find_one({"_id": str(ctx.author.id)})
	  if amount > findbal["wallet"]:
	    await ctx.send("You don't have that much money!")
	  else:
	    collection.update_one({"_id": str(ctx.author.id)}, {"$set": {"_id": str(ctx.author.id), "wallet": int(findbal['wallet'] - amount), "bank": int(findbal['bank'] + amount)} })
	  await ctx.send(f"Deposited ``{amount}`` coins.")

	@commands.cooldown(1, 2, commands.BucketType.user)
	@commands.command(aliases=['with'])
	async def withdraw(self, ctx, amount : int):
	  findbal = collection.find_one({"_id": str(ctx.author.id)})
	  if amount > findbal["bank"]:
	    await ctx.send("You don't have that much money!")
	  else:
	    collection.update_one({"_id": str(ctx.author.id)}, {"$set": {"_id": str(ctx.author.id), "wallet": int(findbal['wallet'] + amount), "bank": int(findbal['bank'] - amount)} })
	  await ctx.send(f"Withdrew ``{amount}`` coins.")



	@commands.cooldown(1, 60, commands.BucketType.user)
	@commands.command(aliases=['rob'])
	async def steal(self, ctx, member: discord.Member):
	  victimbal = collection.find_one({"_id": str(member.id)})
	  userbal = collection.find_one({"_id": str(ctx.author.id)})
	  earned = random.randint(1, victimbal['wallet'])
	  collection.update_one({"_id": str(member.id)}, {"$set": {"_id": str(member.id), "wallet": int(victimbal["wallet"] - earned), "bank": int(victimbal["bank"])}})
	  collection.update_one({"_id": str(ctx.author.id)}, {"$set": {"_id": str(ctx.author.id), "wallet": int(userbal['wallet'] + earned), "bank": int(userbal['bank'])}})
	  await ctx.send(f"You stole {earned} from {member.mention}")




def setup(client):
    client.add_cog(economy(client))
