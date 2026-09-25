import discord
from discord import app_commands

from database.zones import (
    creer_zone,
    zone_existe,
    ajouter_pokemon_zone,
    pokemon_existe,
    supprimer_pokemon_zone,
    supprimer_zone,
    lister_pokemons_zone
)

from utilitaire.permission import est_admin


# Charge les commandes liées aux zones
def charger_commandes_zone(bot):

    @bot.tree.command(
        name="zone_creer",
        description="Créer une zone dans le salon actuel"
    )
    @app_commands.describe(
        nom="Nom de la zone"
    )
    async def zone_creer(
        interaction: discord.Interaction,
        nom: str
    ):

        # Vérifie les permissions
        if not est_admin(interaction):
            await interaction.response.send_message(
                "❌ Réservé aux administrateurs.",
                ephemeral=True
            )
            return

        # Crée la zone dans le salon
        creer_zone(
            interaction.channel.id,
            nom
        )

        await interaction.response.send_message(
            f"✅ Zone **{nom}** créée dans ce salon."
        )


    @bot.tree.command(
        name="zone_ajouter_pokemon",
        description="Ajouter un Pokémon à la zone actuelle"
    )
    @app_commands.describe(
        pokemon_id="Numéro du Pokémon",
        chance="Chance d'apparition"
    )
    async def zone_ajouter_pokemon(
        interaction: discord.Interaction,
        pokemon_id: int,
        chance: int
    ):

        # Vérifie les permissions
        if not est_admin(interaction):
            await interaction.response.send_message(
                "❌ Réservé aux administrateurs.",
                ephemeral=True
            )
            return

        # Vérifie que la zone existe
        if not zone_existe(interaction.channel.id):
            await interaction.response.send_message(
                "❌ Aucune zone n'existe dans ce salon."
            )
            return

        # Vérifie que le Pokémon existe
        if not pokemon_existe(pokemon_id):
            await interaction.response.send_message(
                f"❌ Pokémon #{pokemon_id} introuvable."
            )
            return

        # Ajoute le Pokémon à la zone
        ajouter_pokemon_zone(
            interaction.channel.id,
            pokemon_id,
            chance
        )

        await interaction.response.send_message(
            f"✅ Pokémon #{pokemon_id} ajouté "
            f"avec une chance d'apparition de {chance}."
        )


    @bot.tree.command(
        name="zone_liste_pokemons",
        description="Liste les Pokémon de la zone actuelle"
    )
    async def zone(
        interaction: discord.Interaction
    ):

        # Vérifie que la zone existe
        if not zone_existe(interaction.channel.id):
            await interaction.response.send_message(
                "❌ Aucune zone dans ce salon."
            )
            return

        # Récupère les Pokémon de la zone
        pokemons = lister_pokemons_zone(
            interaction.channel.id
        )

        if not pokemons:
            await interaction.response.send_message(
                "❌ Aucun Pokémon configuré dans cette zone."
            )
            return

        # Prépare la liste des Pokémon
        texte = "🌿 **Pokémon de la zone**\n\n"

        for p in pokemons:
            texte += (
                f"#{p['id']} "
                f"{p['name']} "
                f"(Chance : {p['chance']})\n"
            )

        await interaction.response.send_message(texte)


    @bot.tree.command(
        name="zone_supprimer_pokemon",
        description="Retirer un Pokémon de la zone"
    )
    @app_commands.describe(
        pokemon_id="Numéro du Pokémon"
    )
    async def zone_supprimer_pokemon(
        interaction: discord.Interaction,
        pokemon_id: int
    ):

        # Vérifie les permissions
        if not est_admin(interaction):
            await interaction.response.send_message(
                "❌ Réservé aux administrateurs.",
                ephemeral=True
            )
            return

        # Supprime le Pokémon de la zone
        success = supprimer_pokemon_zone(
            interaction.channel.id,
            pokemon_id
        )

        if success:
            await interaction.response.send_message(
                f"✅ Pokémon #{pokemon_id} retiré de la zone."
            )
        else:
            await interaction.response.send_message(
                f"❌ Pokémon #{pokemon_id} absent de cette zone."
            )


    @bot.tree.command(
        name="zone_supprimer",
        description="Supprimer la zone actuelle"
    )
    async def zone_supprimer(
        interaction: discord.Interaction
    ):

        # Vérifie les permissions
        if not est_admin(interaction):
            await interaction.response.send_message(
                "❌ Réservé aux administrateurs.",
                ephemeral=True
            )
            return

        # Vérifie que la zone existe
        if not zone_existe(interaction.channel.id):
            await interaction.response.send_message(
                "❌ Aucune zone à supprimer."
            )
            return

        # Supprime la zone
        supprimer_zone(
            interaction.channel.id
        )

        await interaction.response.send_message(
            "✅ Zone supprimée."
        )