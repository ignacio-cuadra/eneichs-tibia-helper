import re
import discord
import asyncio
from config import DISCORD_TOKEN, GUILD_ID
from scraper import retrieve_players

intents = discord.Intents.default()
intents.guilds = True
intents.members = True 
intents.presences = True 

client = discord.Client(intents=intents)

def vocationInitials(vocation):
  if vocation == "Master Sorcerer":
    return "🔥"
  if vocation == "Elder Druid":
    return "🌿"
  if vocation == "Royal Paladin":
    return "🏹"
  if vocation == "Elite Knight":
    return "🔰"
  return "UNK"

async def update_nickname(member, players):
  current_name = member.display_name
  #remove all after last character does not match a letter, number, space, underscore or dash or '

  filtered_name = re.match(r"^[a-zA-Z0-9_'\-\s]+", current_name)
  if filtered_name:
    current_name = filtered_name.group()
  current_name = current_name.strip()
  #find player in players list that has the same name as the current_name
  player = next((p for p in players if p["name"] == current_name), None)

  if player is None:
    # print(f"❌ No se encontró el jugador {current_name} en la lista de jugadores")
    return
  new_name = f"{player['name']}{vocationInitials(player['vocation'])}{player['level']}"
  if (new_name == member.display_name):
    return
  try:
    print (f"✏️ {member.display_name} → {new_name}")
    await member.edit(nick=new_name)
    print(f"✅ Apodo cambiado")
  except discord.Forbidden as e:
    print(f"❌ No tengo permiso para cambiar el apodo de {member.name}")
    
async def update_nicknames():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)

    if guild is None:
        print("❌ No se encontró el servidor. Verifica GUILD_ID en .env")
        return

    while not client.is_closed():
        try:
            players = retrieve_players()
            if not players:
                print("⚠️ No se encontraron nombres en el scraping.")
                await asyncio.sleep(60 * 10)
                continue
            # number of players
            print(f"🔍 Se encontraron {len(players)} jugadores")
            for member in guild.members:
                if member.bot:
                    continue
                await update_nickname(member, players)

        except Exception as e:
            print(f"⚠️ Error en la actualización de apodos: {e}")

        await asyncio.sleep(60 * 1)

@client.event
async def on_ready():
    print(f"✅ Bot conectado como {client.user}")
    client.loop.create_task(update_nicknames())

client.run(DISCORD_TOKEN)