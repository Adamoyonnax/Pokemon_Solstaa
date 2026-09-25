import sqlite3
import os


# Définit le chemin vers la base de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "pokemon.db")


# Ouvre une connexion à la base de données
def get_connection():
    conn = sqlite3.connect(DB_PATH)

    # Permet d'utiliser les noms des colonnes
    conn.row_factory = sqlite3.Row

    return conn


# Crée les tables si elles n'existent pas
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Informations des joueurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            discord_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            personnage TEXT NOT NULL,
            money INTEGER DEFAULT 1000,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Liste des Pokémon disponibles dans le jeu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pokemons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            image TEXT NOT NULL
        )
    """)

    # Informations sur les évolutions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evolutions (
            pokemon_id INTEGER NOT NULL,
            evolution_id INTEGER NOT NULL,
            niveau INTEGER NOT NULL,
            PRIMARY KEY (pokemon_id, evolution_id)
        )
    """)

    # Pokémon possédés par les joueurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_pokemons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            pokemon_id INTEGER NOT NULL,
            shiny INTEGER NOT NULL DEFAULT 0,
            talent_cache INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Zones disponibles dans les salons Discord
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS zones (
            channel_id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL
        )
    """)

    # Pokémon pouvant apparaître dans chaque zone
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS zone_pokemons (
            channel_id INTEGER,
            pokemon_id INTEGER,
            chance INTEGER,
            PRIMARY KEY(channel_id, pokemon_id)
        )
    """)

    # Inventaire des balls de chaque joueur
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventories (
            player_id INTEGER PRIMARY KEY,
            pokeball INTEGER DEFAULT 5,
            superball INTEGER DEFAULT 0,
            hyperball INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
