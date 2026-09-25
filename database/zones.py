from database.db import get_connection


# Crée une zone dans un salon Discord
def creer_zone(channel_id, nom):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO zones (channel_id, nom)
        VALUES (?, ?)
    """, (channel_id, nom))

    conn.commit()
    conn.close()


# Vérifie si une zone existe
def zone_existe(channel_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM zones
        WHERE channel_id = ?
    """, (channel_id,))

    zone = cursor.fetchone()

    conn.close()

    return zone


# Ajoute un Pokémon dans une zone
# "chance" indique sa fréquence d'apparition
def ajouter_pokemon_zone(channel_id, pokemon_id, chance):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO zone_pokemons
        (channel_id, pokemon_id, chance)
        VALUES (?, ?, ?)
    """, (channel_id, pokemon_id, chance))

    conn.commit()
    conn.close()


# Vérifie si un Pokémon existe
def pokemon_existe(pokemon_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM pokemons WHERE id = ?",
        (pokemon_id,)
    )

    pokemon = cursor.fetchone()

    conn.close()

    return pokemon


# Supprime une zone et ses Pokémon
def supprimer_zone(channel_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Supprime la zone
    cursor.execute("""
        DELETE FROM zones
        WHERE channel_id = ?
    """, (channel_id,))

    # Supprime les Pokémon de la zone
    cursor.execute("""
        DELETE FROM zone_pokemons
        WHERE channel_id = ?
    """, (channel_id,))

    conn.commit()
    conn.close()


# Supprime un Pokémon d'une zone
def supprimer_pokemon_zone(channel_id, pokemon_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM zone_pokemons
        WHERE channel_id = ? AND pokemon_id = ?
    """, (channel_id, pokemon_id))

    # Vérifie si un Pokémon a été supprimé
    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted


# Affiche les Pokémon présents dans une zone
def lister_pokemons_zone(channel_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.name,
            zp.chance
        FROM zone_pokemons zp
        JOIN pokemons p
            ON p.id = zp.pokemon_id
        WHERE zp.channel_id = ?
        ORDER BY p.id
    """, (channel_id,))

    result = cursor.fetchall()

    conn.close()

    return result


# Récupère les Pokémon disponibles pour le spawn
def get_pokemons_zone(channel_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pokemon_id, chance
        FROM zone_pokemons
        WHERE channel_id = ?
    """, (channel_id,))

    result = cursor.fetchall()

    conn.close()

    return result