import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

@bot.command()
async def top10(ctx):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    message = "**Top 10 Crypto 🔥 :**\n"
    for coin in data:
        name = coin["name"]
        price = coin["current_price"]
        change = coin["price_change_percentage_24h"]
        emoji = "📈" if change >= 0 else "📉"
        message += f"{emoji} **{name}** - ${price:.2f} ({change:.2f}%)\n"

    best = max(data, key=lambda x: x["price_change_percentage_24h"])
    message += f"\n💡 **Suggestion d'investissement :** `{best['name']}` (+{best['price_change_percentage_24h']:.2f}%)"

    await ctx.send(message)

bot.run(TOKEN)
