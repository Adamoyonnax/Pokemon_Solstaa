import discord

from database.player import (
    create_player,
    get_player,
    get_inventory
)

from database.player_pokemon import (
    lister_pokemons_sql
)

from vue.boutonListe import PokemonListeView


# Charge les commandes liées aux joueurs
def charger_commandes_player(bot):

    @bot.tree.command(
        name="commencer",
        description="Créer un personnage"
    )
    async def commencer(
        interaction: discord.Interaction,
        nom: str
    ):

        # Crée le joueur dans la base de données
        create_player(
            interaction.user,
            nom
        )

        await interaction.response.send_message(
            f"Profil créé pour {nom}"
        )


    @bot.tree.command(
        name="profil",
        description="Afficher ton profil joueur"
    )
    async def profil(
        interaction: discord.Interaction
    ):

        # Récupère les informations du joueur
        player = get_player(
            interaction.user
        )

        # Récupère son inventaire
        inventory = get_inventory(
            interaction.user.id
        )

        # Vérifie que le joueur existe
        if not player:
            await interaction.response.send_message(
                "❌ Tu n'as pas encore de personnage. "
                "Utilise /commencer"
            )
            return

        # Crée l'affichage du profil
        embed = discord.Embed(
            title="🎮 Profil Joueur"
        )

        embed.add_field(
            name="👤 Joueur",
            value=player["username"],
            inline=False
        )

        embed.add_field(
            name="🧙 Personnage",
            value=player["personnage"],
            inline=False
        )

        embed.add_field(
            name="💰 Money",
            value=player["money"],
            inline=False
        )

        embed.add_field(
            name="🎒 Inventaire",
            value=(
                f"🔴 Poké Balls : {inventory['pokeball']}\n"
                f"🔵 Super Balls : {inventory['superball']}\n"
                f"🟡 Hyper Balls : {inventory['hyperball']}"
            ),
            inline=False
        )

        await interaction.response.send_message(
            embed=embed
        )


    @bot.tree.command(
        name="pokedex",
        description="Afficher tes Pokémon"
    )
    async def pokedex(
        interaction: discord.Interaction
    ):

        # Récupère les Pokémon du joueur
        pokemons = lister_pokemons_sql(
            interaction.user.id
        )

        # Vérifie si le joueur possède des Pokémon
        if not pokemons:
            await interaction.response.send_message(
                "Tu n'as aucun Pokémon."
            )
            return

        # Crée la liste avec 10 Pokémon par page
        view = PokemonListeView(
            pokemons,
            par_page=10
        )

        # Affiche la première page
        await interaction.response.send_message(
            embed=view.creer_embed(),
            view=view
        )

        # Récupère le message pour les boutons
        view.message = await interaction.original_response()