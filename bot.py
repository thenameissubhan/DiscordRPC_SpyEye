import discord
import requests
from discord.ext import commands

# Bot setup
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# RPC API URL (replace with your Flask app's URL)
RPC_API_URL = "http://localhost:5000"

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.command()
async def set_status(ctx, *, status):
    """
    Set a custom status for the Discord RPC.
    """
    user_id = ctx.author.id
    data = {"user_id": user_id, "status": status}
    response = requests.post(f"{RPC_API_URL}/set-status", json=data)

    if response.status_code == 200:
        await ctx.send(f"Status updated to: {status}")
    else:
        await ctx.send("Failed to update status.")

@bot.command()
async def link_rpc(ctx, code):
    """
    Link the bot with the RPC using a unique code.
    """
    user_id = ctx.author.id
    data = {"user_id": user_id, "code": code}
    response = requests.post(f"{RPC_API_URL}/link", json=data)

    if response.status_code == 200:
        await ctx.send("RPC linked successfully!")
    else:
        await ctx.send("Failed to link RPC. Please try again.")

# Run the bot (replace with your bot token)
bot.run("MTMyMDQ0NzkwMTIxNzg1MzQ1MA.GaZur6.RJZaCh1ycjXtx38D5tSLQlMFjpMeimvKwlp47k")
