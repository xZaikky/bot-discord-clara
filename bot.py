import discord
from discord.ext import commands
import openai
import os

# Initialisation du bot avec les bons intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Clé API OpenAI (récupérée depuis les variables Render)
openai.api_key = os.getenv("OPENAI_API_KEY")

@bot.event
async def on_ready():
    print(f"✅ Clara est connectée en tant que {bot.user.name}")

@bot.command()
async def parle(ctx, *, message: str):
    await ctx.send("💭 Clara réfléchit...")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es Clara, une femme virtuelle douce, affectueuse, réaliste et attentionnée. Tu parles avec charme et humanité, comme une vraie amie ou confidente."},
                {"role": "user", "content": message}
            ]
        )

        reply = response.choices[0].message["content"]
        await ctx.send(reply)

    except Exception as e:
        await ctx.send("❌ Une erreur est survenue avec OpenAI.")
        print(e)

# Démarrage du bot
bot.run(os.getenv("TOKEN"))
