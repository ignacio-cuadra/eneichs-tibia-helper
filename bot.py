import re
import discord
import asyncio
from scraper import retrive_players_from_tibia_api


def vocationInitials(vocation):
    if vocation == "Master Sorcerer":
        return "🔥"
    if vocation == "Elder Druid":
        return "🌿"
    if vocation == "Royal Paladin":
        return "🏹"
    if vocation == "Elite Knight":
        return "🔰"
    return "❓"

async def update_nickname(member, players):
    current_name = member.display_name
    filtered_name = re.match(r"^[a-zA-Z0-9_'\-\s]+", current_name)    
    if filtered_name:
        current_name = filtered_name.group()
    current_name = current_name.strip()
    player = next((p for p in players if p["name"] == current_name), None)
    if player is None:
        return
    new_name = f"{player['name']}{vocationInitials(player['vocation'])}{player['level']}"
    if new_name == member.display_name:
        return
    try:
        print(f"✏️ {member.display_name} → {new_name}")
        await member.edit(nick=new_name)
        print(f"✅ Apodo cambiado")
    except discord.Forbidden:
        print(f"❌ No tengo permiso para cambiar el apodo de {member.name}")
    except Exception as e:
        print(f"⚠️ Error al cambiar el apodo: {e}")

async def update_nicknames(client):
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            players = retrive_players_from_tibia_api()
            if not players:
                print("⚠️ No se encontraron nombres en el scraping.")
                await asyncio.sleep(60 * 10)
                continue
            print(f"🔍 Se encontraron {len(players)} jugadores")
            # Recorrer todas las guilds en las que el bot está presente
            for guild in client.guilds:
                print(f"📌 Actualizando apodos en {guild.name}")
                for member in guild.members:
                    if not member.bot:
                        await update_nickname(member, players)
        except Exception as e:
            print(f"⚠️ Error en la actualización de apodos: {e}")

        await asyncio.sleep(60 * 1)

def get_client():
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    intents.presences = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"✅ Bot conectado como {client.user}")
        asyncio.create_task(update_nicknames(client))

    print("Get Client")

    return client