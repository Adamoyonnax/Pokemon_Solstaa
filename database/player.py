from database.db import get_connection


# Crée un joueur et son inventaire
def create_player(user, personnage):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO players
        (discord_id, username, personnage)
        VALUES (?, ?, ?)
        """,
        (user.id, user.name, personnage)
    )

    # Crée l'inventaire du joueur
    cursor.execute(
        """
        INSERT OR IGNORE INTO inventories
        (player_id)
        VALUES (?)
        """,
        (user.id,))

    conn.commit()
    conn.close()


# Récupère les informations d'un joueur
def get_player(user):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT discord_id, username, personnage, money
        FROM players
        WHERE discord_id = ?
        """,
        (user.id,)
    )

    row = cursor.fetchone()
    conn.close()

    return row


# Récupère l'inventaire d'un joueur
def get_inventory(player_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pokeball, superball, hyperball
        FROM inventories
        WHERE player_id = ?
    """, (player_id,))

    row = cursor.fetchone()
    conn.close()

    # Retourne 0 si l'inventaire n'existe pas
    if row is None:
        return {
            "pokeball": 0,
            "superball": 0,
            "hyperball": 0
        }

    return row


# Ajoute des balls à l'inventaire
def ajouter_ball(player_id, type_ball, nombre):
    conn = get_connection()
    cursor = conn.cursor()

    # Choisit la colonne correspondant au type de ball
    if type_ball == "Pokéball":
        colonne = "pokeball"
    elif type_ball == "Superball":
        colonne = "superball"
    elif type_ball == "Hyperball":
        colonne = "hyperball"
    else:
        conn.close()
        return False

    cursor.execute(
        f"""
        UPDATE inventories
        SET {colonne} = {colonne} + ?
        WHERE player_id = ?
        """,
        (nombre, player_id)
    )

    conn.commit()
    conn.close()

    return True


# Retire des balls de l'inventaire
def retirer_ball(player_id, type_ball, nombre):
    conn = get_connection()
    cursor = conn.cursor()

    # Choisit la colonne correspondant au type de ball
    if type_ball == "Pokéball":
        colonne = "pokeball"
    elif type_ball == "Superball":
        colonne = "superball"
    elif type_ball == "Hyperball":
        colonne = "hyperball"
    else:
        conn.close()
        return False

    # Vérifie que le joueur possède suffisamment de balls
    cursor.execute(
        f"""
        SELECT {colonne}
        FROM inventories
        WHERE player_id = ?
        """,
        (player_id,)
    )

    inventory = cursor.fetchone()

    if inventory is None:
        conn.close()
        return False

    if inventory[0] < nombre:
        conn.close()
        return False

    cursor.execute(
        f"""
        UPDATE inventories
        SET {colonne} = {colonne} - ?
        WHERE player_id = ?
        """,
        (nombre, player_id)
    )

    conn.commit()
    conn.close()

    return True


# Ajoute de l'argent au joueur
def ajouter_argent(player_id, montant):

    # Le montant doit être positif
    if montant <= 0:
        return False

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE players
        SET money = money + ?
        WHERE discord_id = ?
        """,
        (montant, player_id)
    )

    succes = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return succes


# Retire de l'argent au joueur
def retirer_argent(player_id, montant):

    # Le montant doit être positif
    if montant <= 0:
        return False

    conn = get_connection()
    cursor = conn.cursor()

    # Vérifie que le joueur possède assez d'argent
    cursor.execute(
        """
        SELECT money
        FROM players
        WHERE discord_id = ?
        """,
        (player_id,)
    )

    player = cursor.fetchone()

    if player is None:
        conn.close()
        return False

    if player["money"] < montant:
        conn.close()
        return False

    cursor.execute(
        """
        UPDATE players
        SET money = money - ?
        WHERE discord_id = ?
        """,
        (montant, player_id)
    )

    conn.commit()
    conn.close()

    return True