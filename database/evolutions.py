from database.db import get_connection


# Associe chaque badge Discord à un niveau maximum
BADGES = {
    1553000841710018630: 20,
    1553000902304997487: 30,
    1553000920797683742: 40,
    1553000940410245120: 50,
    1553000954973126686: 60,
    1553000971058020443: 70,
    1553000991207465020: 80,
    1553001017338101920: 90
}


# Ajoute l'évolution d'un Pokémon à la collection
def evoluer_pokemon_sql(
    player_id,
    evolution_id,
    shiny,
    talent_cache
):
    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Vérifie si l'évolution existe déjà
        cursor.execute(
            """
            SELECT id
            FROM player_pokemons
            WHERE player_id = ?
            AND pokemon_id = ?
            AND shiny = ?
            AND talent_cache = ?
            """,
            (
                player_id,
                evolution_id,
                int(shiny),
                int(talent_cache)
            )
        )

        existe = cursor.fetchone()

        # Ajoute l'évolution si elle n'existe pas
        if not existe:

            cursor.execute(
                """
                INSERT INTO player_pokemons
                (player_id, pokemon_id, shiny, talent_cache)
                VALUES (?, ?, ?, ?)
                """,
                (
                    player_id,
                    evolution_id,
                    int(shiny),
                    int(talent_cache)
                )
            )

        conn.commit()

    # Annule les modifications en cas d'erreur
    except Exception:
        conn.rollback()
        raise

    # Ferme toujours la connexion
    finally:
        conn.close()


# Détermine le niveau maximum selon les badges du joueur
def get_niveau_max_badge(member):

    badge_obtenu = 0
    niveau_max = 0

    # Parcourt tous les badges
    for index, (role_id, niveau) in enumerate(
        BADGES.items(),
        start=1
    ):

        # Vérifie si le joueur possède le badge
        if any(role.id == role_id for role in member.roles):

            # Garde le badge donnant le niveau maximum
            if niveau > niveau_max:
                niveau_max = niveau
                badge_obtenu = index

    return badge_obtenu, niveau_max