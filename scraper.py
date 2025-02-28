import requests
from bs4 import BeautifulSoup
from config import WORLD
import re

def clean_text(text):
  return re.sub(r'[\x00-\x1F\x7F\xA0]+', ' ', text).strip()

def retrieve_players():
  try:
    response = requests.get("https://www.tibia.com/community/?subtopic=worlds&world=" + WORLD)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("#worlds .Table2 .Odd, #worlds .Table2 .Even")
    players = []
    for row in rows:
      cols = row.find_all("td")
      if len(cols) >= 3:
        players.append({
          "name": clean_text(cols[0].text),
          "level": clean_text(cols[1].text),
          "vocation": clean_text(cols[2].text)
        })
    return players
  except Exception as e:
    print(f"⚠️ Error en el scraping: {e}")
    return []
    

retrieve_players()