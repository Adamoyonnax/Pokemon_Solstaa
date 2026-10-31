
import random
import time

from database.db import get_connection


# Effectue une fouille et attribue la récompense
def effectuer_fouille(player_id):
    recompenses = [
        {"type": "pokeball", "quantite": 5, "poids": 40},
        {"type": "superball", "quantite": 3, "poids": 20},
        {"type": "objet", "rang": "D", "poids": 15},
        {"type": "argent", "quantite": 1500, "poids": 10},
        {"type": "objet", "rang": "C", "poids": 10},
        {"type": "objet", "rang": "B", "poids": 5}
    ]

    delai = 12 * 60 * 60
    maintenant = time.time()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Crée la table des délais de fouille
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fouilles (
                player_id INTEGER PRIMARY KEY,
                derniere_fouille REAL NOT NULL
            )
        """)

        # Empêche deux fouilles simultanées
        cursor.execute("BEGIN IMMEDIATE")

        # Vérifie que le joueur possède un profil
        cursor.execute("""
            SELECT discord_id
            FROM players
            WHERE discord_id = ?
        """, (player_id,))

        if cursor.fetchone() is None:
            conn.rollback()
            return {"status": "no_player"}

        # Vérifie le délai de recharge
        cursor.execute("""
            SELECT derniere_fouille
            FROM fouilles
            WHERE player_id = ?
        """, (player_id,))

        derniere_fouille = cursor.fetchone()

        if derniere_fouille:
            temps_restant = delai - (
                maintenant - derniere_fouille["derniere_fouille"]
            )

            if temps_restant > 0:
                conn.rollback()
                return {
                    "status": "cooldown",
                    "remaining": int(temps_restant)
                }

        # Tire une récompense aléatoire
        recompense = random.choices(
            recompenses,
            weights=[r["poids"] for r in recompenses],
            k=1
        )[0]

        # Ajoute les Pokéballs
        if recompense["type"] == "pokeball":
            cursor.execute("""
                INSERT OR IGNORE INTO inventories (player_id)
                VALUES (?)
            """, (player_id,))

            cursor.execute("""
                UPDATE inventories
                SET pokeball = pokeball + ?
                WHERE player_id = ?
            """, (recompense["quantite"], player_id))

        # Ajoute les Superballs
        elif recompense["type"] == "superball":
            cursor.execute("""
                INSERT OR IGNORE INTO inventories (player_id)
                VALUES (?)
            """, (player_id,))

            cursor.execute("""
                UPDATE inventories
                SET superball = superball + ?
                WHERE player_id = ?
            """, (recompense["quantite"], player_id))

        # Ajoute l'argent
        elif recompense["type"] == "argent":
            cursor.execute("""
                UPDATE players
                SET money = money + ?
                WHERE discord_id = ?
            """, (recompense["quantite"], player_id))

        # Enregistre la date de la dernière fouille
        cursor.execute("""
            INSERT OR REPLACE INTO fouilles
            (player_id, derniere_fouille)
            VALUES (?, ?)
        """, (player_id, maintenant))

        conn.commit()

        return {
            "status": "success",
            "recompense": recompense
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

# Permet à un joueur de gagner de l'argent après une rencontre
def effectuer_rencontre_dresseur(player_id):
    recompenses = [
        {"montant": 250, "poids": 40},
        {"montant": 500, "poids": 30},
        {"montant": 750, "poids": 15},
        {"montant": 1000, "poids": 10},
        {"montant": 1500, "poids": 5}
    ]

    delai = 23 * 60 * 60
    maintenant = time.time()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Crée la table des délais
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rencontres_dresseur (
                player_id INTEGER PRIMARY KEY,
                derniere_rencontre REAL NOT NULL
            )
        """)

        # Empêche plusieurs utilisations simultanées
        cursor.execute("BEGIN IMMEDIATE")

        # Vérifie que le joueur possède un profil
        cursor.execute("""
            SELECT discord_id
            FROM players
            WHERE discord_id = ?
        """, (player_id,))

        if cursor.fetchone() is None:
            conn.rollback()
            return {"status": "no_player"}

        # Vérifie le cooldown
        cursor.execute("""
            SELECT derniere_rencontre
            FROM rencontres_dresseur
            WHERE player_id = ?
        """, (player_id,))

        derniere_rencontre = cursor.fetchone()

        if derniere_rencontre:
            temps_restant = delai - (
                maintenant - derniere_rencontre["derniere_rencontre"]
            )

            if temps_restant > 0:
                conn.rollback()
                return {
                    "status": "cooldown",
                    "remaining": int(temps_restant)
                }

        # Tire un gain aléatoire
        recompense = random.choices(
            recompenses,
            weights=[r["poids"] for r in recompenses],
            k=1
        )[0]

        montant = recompense["montant"]

        # Ajoute l'argent au joueur
        cursor.execute("""
            UPDATE players
            SET money = money + ?
            WHERE discord_id = ?
        """, (montant, player_id))

        # Enregistre la date de la rencontre
        cursor.execute("""
            INSERT OR REPLACE INTO rencontres_dresseur
            (player_id, derniere_rencontre)
            VALUES (?, ?)
        """, (player_id, maintenant))

        conn.commit()

        return {
            "status": "success",
            "montant": montant
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


