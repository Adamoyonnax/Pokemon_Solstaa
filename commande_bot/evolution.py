import discord

from database.player_pokemon import (
    get_connection,
    lister_pokemons_sql
)

from database.evolutions import (
    get_niveau_max_badge,
    evoluer_pokemon_sql
)


# Charge la commande d'évolution
def charger_commandes_evolution(bot):

    @bot.tree.command(
        name="evolution",
        description="Fait évoluer les Pokémon selon les badges obtenus"
    )
    async def evolution(interaction: discord.Interaction):

        # Récupère le profil Discord du joueur
        member = interaction.guild.get_member(
            interaction.user.id
        )

        if member is None:
            await interaction.response.send_message(
                "❌ Impossible de récupérer ton profil Discord.",
                ephemeral=True
            )
            return

        # Récupère le badge et le niveau maximum
        badge, niveau_max = get_niveau_max_badge(member)

        if badge == 0:
            await interaction.response.send_message(
                "❌ Tu ne possèdes aucun badge.",
                ephemeral=True
            )
            return

        # Récupère les Pokémon du joueur
        pokemons = lister_pokemons_sql(
            interaction.user.id
        )

        if not pokemons:
            await interaction.response.send_message(
                "❌ Tu ne possèdes aucun Pokémon.",
                ephemeral=True
            )
            return

        # Liste les évolutions effectuées
        evolutions_effectuees = []

        # Parcourt les Pokémon du joueur
        for pokemon in pokemons:

            pokemon_id = pokemon["id"]
            pokemon_name = pokemon["name"]

            shiny = pokemon["shiny"]
            talent_cache = pokemon["talent_cache"]

            conn = get_connection()
            cursor = conn.cursor()

            # Cherche une évolution possible
            cursor.execute(
                """
                SELECT evolution_id, niveau
                FROM evolutions
                WHERE pokemon_id = ?
                AND niveau <= ?
                ORDER BY niveau DESC
                LIMIT 1
                """,
                (
                    pokemon_id,
                    niveau_max
                )
            )

            evolution = cursor.fetchone()

            conn.close()

            # Aucune évolution disponible
            if evolution is None:
                continue

            evolution_id = evolution["evolution_id"]
            niveau_evolution = evolution["niveau"]

            # Récupère le nom de l'évolution
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, name
                FROM pokemons
                WHERE id = ?
                """,
                (evolution_id,)
            )

            pokemon_evolution = cursor.fetchone()

            conn.close()

            if pokemon_evolution is None:
                continue

            # Ajoute l'évolution à la collection
            evoluer_pokemon_sql(
                interaction.user.id,
                evolution_id,
                shiny,
                talent_cache
            )

            # Enregistre l'évolution pour l'affichage
            evolutions_effectuees.append({
                "pokemon_id": pokemon_id,
                "pokemon_name": pokemon_name,
                "evolution_id": pokemon_evolution["id"],
                "evolution_name": pokemon_evolution["name"],
                "niveau": niveau_evolution,
                "shiny": shiny,
                "talent_cache": talent_cache
            })

        # Vérifie si une évolution a été effectuée
        if not evolutions_effectuees:

            await interaction.response.send_message(
                f"🏅 Tu possèdes le **Badge {badge}**.\n"
                f"📈 Niveau maximum : **{niveau_max}**\n\n"
                f"❌ Aucun de tes Pokémon ne peut évoluer.",
                ephemeral=True
            )

            return

        # Prépare le message des évolutions
        texte = (
            f"🏅 **Badge {badge}**\n"
            f"📈 Niveau maximum : **{niveau_max}**\n\n"
            f"✨ **Évolutions effectuées :**\n\n"
        )

        # Ajoute chaque évolution au message
        for evolution in evolutions_effectuees:

            marqueur = ""

            if evolution["shiny"]:
                marqueur += "✨"

            if evolution["talent_cache"]:
                marqueur += "🔮"

            texte += (
                f"#{evolution['pokemon_id']} "
                f"**{evolution['pokemon_name']}** "
                f"{marqueur}"
                f" → "
                f"#{evolution['evolution_id']} "
                f"**{evolution['evolution_name']}** "
                f"{marqueur}\n"
                f"└ Niveau **{evolution['niveau']}**\n\n"
            )

        # Crée le message final
        embed = discord.Embed(
            title="🌟 Évolution des Pokémon",
            description=texte,
            color=discord.Color.green()
        )

        await interaction.response.send_message(
            embed=embed
        )