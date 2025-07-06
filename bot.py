import discord
from discord import app_commands
from discord.ext import commands
import openai
import os

# Configure les intents
intents = discord.Intents.default()
intents.message_content = True  # Important pour les slash commands
intents.guilds = True

# Crée une classe personnalisée du bot
class ClaraBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()  # Synchronise les slash commands

# Initialise le bot
bot = ClaraBot()

# Récupère la clé OpenAI depuis les variables d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")

# Slash command : /parle
@bot.tree.command(name="parle", description="Parle à Clara (IA)")
@app_commands.describe(message="Ce que tu veux dire à Clara")
async def parle(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("💭 Clara réfléchit...")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Tu peux changer en "gpt-4" si tu as accès
            messages=[
                {"role": "system", "content": "Tu es Clara, une assistante amicale et douce."},
                {"role": "user", "content": message}
            ]
        )

        reply = response['choices'][0]['message']['content']
        await interaction.followup.send(f"🤖 Clara : {reply}")

    except Exception as e:
        print(f"Erreur OpenAI : {e}")
        await interaction.followup.send("❌ Une erreur est survenue avec OpenAI.")

# Démarre le bot
bot.run(os.getenv("DISCORD_TOKEN"))
