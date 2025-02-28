from flask import Flask
from threading import Thread
client = None
app = Flask('')
@app.route('/')
def index():
  return 'Eneich Tibia Helper is online!'

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  print("🌐 Iniciando servidor web")
  server = Thread(target=run)
  server.start()
