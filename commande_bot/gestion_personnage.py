
import discord
from discord import app_commands

from database.player import (
    create_player,
    get_player,
    get_inventory,
    acheter_ball,
    modifier_nom_personnage
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

        # Vérifie que le joueur existe
        if not player:
            await interaction.response.send_message(
                "❌ Tu n'as pas encore de personnage. "
                "Utilise /commencer"
            )
            return

        # Récupère son inventaire
        inventory = get_inventory(
            interaction.user.id
        )

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
        name="acheter_ball",
        description="Acheter des balls avec ton argent"
    )
    @app_commands.describe(
        type_ball="Type de ball à acheter",
        nombre="Quantité à acheter"
    )
    @app_commands.choices(
        type_ball=[
            app_commands.Choice(
                name="🔴 Pokéball - 200",
                value="Pokéball"
            ),
            app_commands.Choice(
                name="🔵 Superball - 500",
                value="Superball"
            ),
            app_commands.Choice(
                name="🟡 Hyperball - 800",
                value="Hyperball"
            )
        ]
    )
    async def acheter_ball_commande(
        interaction: discord.Interaction,
        type_ball: app_commands.Choice[str],
        nombre: int
    ):

        # Vérifie la quantité demandée
        if nombre <= 0:
            await interaction.response.send_message(
                "❌ La quantité doit être supérieure à 0.",
                ephemeral=True
            )
            return

        # Vérifie que le joueur possède un profil
        if not get_player(interaction.user):
            await interaction.response.send_message(
                "❌ Tu dois d'abord créer un personnage avec /commencer.",
                ephemeral=True
            )
            return

        # Effectue l'achat
        succes, prix_total, argent_restant = acheter_ball(
            interaction.user.id,
            type_ball.value,
            nombre
        )

        if not succes:
            await interaction.response.send_message(
                f"❌ Tu n'as pas assez d'argent pour cet achat.\n"
                f"Prix total : **{prix_total}**",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"✅ Achat effectué !\n\n"
            f"🛒 **{nombre}x {type_ball.value}**\n"
            f"💰 Prix total : **{prix_total}**\n"
            f"💵 Argent restant : **{argent_restant}**"
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

    @bot.tree.command(
    name="modifier_nom",
    description="Modifier le nom de ton personnage"
)
    @app_commands.describe(
        nouveau_nom="Le nouveau nom de ton personnage"
    )
    async def modifier_nom(
        interaction: discord.Interaction,
        nouveau_nom: str
    ):

        # Vérifie que le joueur existe
        joueur = get_player(interaction.user.id)

        if not joueur:
            await interaction.response.send_message(
                "❌ Tu n'as pas encore créé de personnage.",
                ephemeral=True
            )
            return

        # Vérifie le nom
        nouveau_nom = nouveau_nom.strip()

        if len(nouveau_nom) < 2 or len(nouveau_nom) > 30:
            await interaction.response.send_message(
                "❌ Le nom doit contenir entre 2 et 30 caractères.",
                ephemeral=True
            )
            return

        # Modifie le nom
        succes = modifier_nom_personnage(
            interaction.user.id,
            nouveau_nom
        )

        if not succes:
            await interaction.response.send_message(
                "❌ Impossible de modifier ton nom.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"✅ Ton personnage porte désormais le nom **{nouveau_nom}** !",
            ephemeral=True
        )

