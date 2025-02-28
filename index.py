import bot
import webserver
import asyncio
from config import DISCORD_TOKEN

client = bot.get_client()
webserver.keep_alive()
client.run(DISCORD_TOKEN)