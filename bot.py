import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user.name}")

@bot.command()
async def parle(ctx, *, message: str):
    await ctx.send(f"Tu m’as dit : {message} 😘")

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
