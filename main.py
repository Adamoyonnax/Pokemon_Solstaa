import discord
import os
from dotenv import load_dotenv

from discord.ext import commands 
from database.db import init_db

from commande_bot.evolution import charger_commandes_evolution
from commande_bot.gestion_personnage import charger_commandes_player
from commande_bot.spawn import charger_commandes_spawn
from commande_bot.commande_admin.ajout_suppresion_pokemons import (charger_commandes_admin_pokemon)
from commande_bot.commande_admin.gestion_ressource import(charger_commandes_gestion_ressource)
from commande_bot.commande_admin.gestion_zone import (charger_commandes_zone)

# ID du Serveur
GUILD_ID = 1553000784717676566

# Charge la Base de Donnée 
init_db()

# Charge le .env
load_dotenv() 
TOKEN = os.getenv("DISCORD_TOKEN")


# Permissions du bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Charge les commandes dans le main.py 
charger_commandes_evolution(bot)
charger_commandes_player(bot)
charger_commandes_spawn(bot)
charger_commandes_admin_pokemon(bot)
charger_commandes_gestion_ressource(bot)
charger_commandes_zone(bot)

# Se déclenche à la connexion du bot  
@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)

    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

    print(f"{bot.user} connecté + sync guild OK")


# lance le bot à partir de son token 
bot.run(TOKEN)
