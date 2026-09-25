import discord
from discord import app_commands

from database.player_pokemon import (
    ajouter_pokemon_sql,
    supprimer_pokemon_sql
)

from utilitaire.permission import est_admin


# Charge les commandes d'administration des Pokémon
def charger_commandes_admin_pokemon(bot):

    @bot.tree.command(
        name="ajouter_pokemon",
        description="Ajouter un Pokémon à un joueur"
    )
    @app_commands.describe(
        joueur="Mention du joueur",
        pokemon_id="ID du Pokémon",
        shiny="1 si le Pokémon est shiny, sinon 0",
        talent_cache="1 si le Pokémon possède le talent caché, sinon 0"
    )
    async def ajouter_pokemon(
        interaction: discord.Interaction,
        joueur: discord.User,
        pokemon_id: int,
        shiny: int = 0,
        talent_cache: int = 0
    ):

        # Vérifie les permissions
        if not est_admin(interaction):
            await interaction.response.send_message(
                "❌ Réservé aux administrateurs.",
                ephemeral=True
            )
            return

        # Ajoute le Pokémon au joueur
        success = ajouter_pokemon_sql(
            joueur.id,
            pokemon_id,
            shiny,
            talent_cache
        )

        if success:
            await interaction.response.send_message(
                f"✅ Pokémon #{pokemon_id} ajouté "
                f"à {joueur.name}"
            )
        else:
            await interaction.response.send_message(
                f"❌ {joueur.name} possède déjà "
                f"le Pokémon #{pokemon_id}"
            )


    @bot.tree.command(
        name="supprimer_pokemon",
        description="Supprimer un Pokémon d'un joueur"
    )
    @app_commands.describe(
        joueur="Mention du joueur",
        pokemon_id="ID du Pokémon"
    )
    async def supprimer_pokemon(
        interaction: discord.Interaction,
        joueur: discord.User,
        pokemon_id: int
    ):

        # Vérifie les permissions
        if not est_admin(interaction):
            await interaction.response.send_message(
                "❌ Réservé aux administrateurs.",
                ephemeral=True
            )
            return

        # Supprime le Pokémon du joueur
        success = supprimer_pokemon_sql(
            joueur.id,
            pokemon_id
        )

        if success:
            await interaction.response.send_message(
                f"✅ Pokémon #{pokemon_id} supprimé "
                f"de {joueur.name}"
            )
        else:
            await interaction.response.send_message(
                f"❌ {joueur.name} ne possède pas "
                f"le Pokémon #{pokemon_id}"
            )