import bot
import webserver
import asyncio
from config import DISCORD_TOKEN

client = bot.get_client()
webserver.keep_alive()
print("🚀 Iniciando bot")
client.run(DISCORD_TOKEN)