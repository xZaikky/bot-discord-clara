import discord
from discord.ext import commands
from discord import app_commands
import openai
import os

TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Slash commands synchronisées ({len(synced)})")
    except Exception as e:
        print(f"❌ Erreur de sync : {e}")

@bot.tree.command(name="parle", description="Fais parler Clara avec GPT")
@app_commands.describe(message="Ce que tu veux dire à Clara")
async def parle(interaction: discord.Interaction, message: str):
    await interaction.response.defer()  # optionnel si GPT prend du temps

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        text = response.choices[0].message.content
        await interaction.followup.send(text)
    except Exception as e:
        print(f"Erreur GPT : {e}")
        await interaction.followup.send("❌ Une erreur est survenue avec OpenAI.")

bot.run(TOKEN)
