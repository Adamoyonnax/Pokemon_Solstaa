from database.db import get_connection


# Associe chaque badge Discord à un niveau maximum
BADGES = {
    1553303638586429520: 20,
    1553303688079216642: 30,
    1553303717954981968: 40,
    1553303758186741821: 50,
    1553303794031267941: 60,
    1553304533461893200: 65,
    1553304569868714024: 70,
    1553304607206416434: 75,
    1553304636126011473: 80,
    1553304686784815165: 85,
    1553304776891170918: 90,
    1553304810139160696: 95
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