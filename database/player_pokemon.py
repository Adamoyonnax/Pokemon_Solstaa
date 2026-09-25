from database.db import get_connection


# Ajoute un Pokémon à la collection d'un joueur
def ajouter_pokemon_sql( player_id, pokemon_id, shiny, talent_cache ):

    conn = get_connection()
    cursor = conn.cursor()

    # Vérifie si cette version du Pokémon existe déjà
    cursor.execute("""
        SELECT id
        FROM player_pokemons
        WHERE player_id = ?
        AND pokemon_id = ?
        AND shiny = ?
        AND talent_cache = ?
        """,
        (player_id, pokemon_id, int(shiny), int(talent_cache)))

    existe = cursor.fetchone()

    # Le Pokémon existe déjà
    if existe:
        conn.close()
        return False

    # Ajoute le Pokémon à la collection
    cursor.execute("""
        INSERT INTO player_pokemons
        (player_id, pokemon_id, shiny, talent_cache)
        VALUES (?, ?, ?, ?)
        """,
        (player_id, pokemon_id, int(shiny), int(talent_cache)))

    conn.commit()
    conn.close()

    return True


# Supprime un Pokémon de la collection
def supprimer_pokemon_sql(player_id, pokemon_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Vérifie que le joueur possède le Pokémon
    cursor.execute("""
        SELECT 1
        FROM player_pokemons
        WHERE player_id = ? AND pokemon_id = ?
    """, (player_id, pokemon_id))

    if not cursor.fetchone():
        conn.close()
        return False

    # Supprime le Pokémon
    cursor.execute("""
        DELETE FROM player_pokemons
        WHERE player_id = ? AND pokemon_id = ?
    """, (player_id, pokemon_id))

    conn.commit()
    conn.close()

    return True


# Récupère la liste des Pokémon d'un joueur
def lister_pokemons_sql(player_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.id, p.name, shiny, talent_cache
        FROM player_pokemons pp
        JOIN pokemons p ON pp.pokemon_id = p.id
        WHERE pp.player_id = ?
        ORDER BY p.id ASC
    """, (player_id,))

    rows = cursor.fetchall()
    conn.close()

    return rows


# Récupère les informations d'un Pokémon
def get_pokemon(pokemon_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM pokemons
        WHERE id = ?
    """, (pokemon_id,))

    pokemon = cursor.fetchone()

    conn.close()

    return pokemon


# Utilise une Pokéball de l'inventaire
def utiliser_pokeball(player_id, type_ball):
    conn = get_connection()
    cursor = conn.cursor()

    # Vérifie que le type de ball est valide
    if type_ball not in ["pokeball", "superball", "hyperball"]:
        conn.close()
        return False

    # Retire une ball si le joueur en possède au moins une
    cursor.execute(
        f"""
        UPDATE inventories
        SET {type_ball} = {type_ball} - 1
        WHERE player_id = ?
        AND {type_ball} > 0
        """,
        (player_id,)
    )

    utilisee = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return utilisee