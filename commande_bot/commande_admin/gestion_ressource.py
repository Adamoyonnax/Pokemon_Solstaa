import discord
from discord import app_commands

from database.player import (
    ajouter_ball as db_ajouter_ball,
    retirer_ball as db_retirer_ball,
    ajouter_argent as db_ajouter_argent,
    retirer_argent as db_retirer_argent,
    payer_joueur as db_payer_joueur
)

from utilitaire.permission import est_admin


# Charge les commandes de gestion des ressources
def charger_commandes_gestion_ressource(bot):

    @bot.tree.command(
        name="ajouter_ball",
        description="Ajouter des Pokéballs à un joueur"
    )
    @app_commands.describe(
        joueur="Le joueur qui recevra les Pokéballs",
        type_ball="Le type de Pokéball",
        nombre="Le nombre de Pokéballs à ajouter"
    )
    @app_commands.choices(
        type_ball=[
            app_commands.Choice(
                name="🔴 Pokéball",
                value="Pokéball"
            ),
            app_commands.Choice(
                name="🔵 Superball",
                value="Superball"
            ),
            app_commands.Choice(
                name="🟡 Hyperball",
                value="Hyperball"
            )
        ]
    )
    async def ajouter_ball(
        interaction: discord.Interaction,
        joueur: discord.Member,
        type_ball: app_commands.Choice[str],
        nombre: int
    ):

        # Vérifie les permissions
        if not est_admin(interaction):
            await interaction.response.send_message(
                "❌ Tu dois être administrateur "
                "ou posséder le rôle autorisé "
                "pour utiliser cette commande.",
                ephemeral=True
            )
            return

        # Vérifie que le nombre est valide
        if nombre <= 0:
            await interaction.response.send_message(
                "❌ Le nombre doit être supérieur à 0.",
                ephemeral=True
            )
            return

        # Ajoute les balls au joueur
        succes = db_ajouter_ball(
            joueur.id,
            type_ball.value,
            nombre
        )

        if not succes:
            await interaction.response.send_message(
                "❌ Type de Pokéball invalide.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"✅ **{nombre} {type_ball.value}** "
            f"ont été ajoutées à {joueur.mention}."
        )
    
    @bot.tree.command(
        name="retirer_ball",
        description="Retirer des Pokéballs à un joueur"
    )
    @app_commands.describe(
        joueur="Le joueur à qui retirer les Pokéballs",
        type_ball="Le type de Pokéball",
        nombre="Le nombre de Pokéballs à retirer"
    )
    @app_commands.choices(
        type_ball=[
            app_commands.Choice(
                name="🔴 Pokéball",
                value="Pokéball"
            ),
            app_commands.Choice(
                name="🔵 Superball",
                value="Superball"
            ),
            app_commands.Choice(
                name="🟡 Hyperball",
                value="Hyperball"
            )
        ]
    )
    async def retirer_ball(
        interaction: discord.Interaction,
        joueur: discord.Member,
        type_ball: app_commands.Choice[str],
        nombre: int
    ):

        # Vérifie les permissions
        if not est_admin(interaction):
            await interaction.response.send_message(
                "❌ Tu dois être administrateur "
                "ou posséder le rôle autorisé "
                "pour utiliser cette commande.",
                ephemeral=True
            )
            return

        # Vérifie que le nombre est valide
        if nombre <= 0:
            await interaction.response.send_message(
                "❌ Le nombre doit être supérieur à 0.",
                ephemeral=True
            )
            return

        # Retire les balls du joueur
        succes = db_retirer_ball(
            joueur.id,
            type_ball.value,
            nombre
        )

        if not succes:
            await interaction.response.send_message(
                f"❌ {joueur.mention} ne possède pas assez "
                f"de {type_ball.value}.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"✅ **{nombre} {type_ball.value}** "
            f"ont été retirées à {joueur.mention}."
        )


    @bot.tree.command(
        name="payer",
        description="Envoyer de l'argent à un autre joueur"
    )
    @app_commands.describe(
        joueur="Joueur qui recevra l'argent",
        montant="Montant à envoyer"
    )
    async def payer(
        interaction: discord.Interaction,
        joueur: discord.Member,
        montant: int
    ):

        # Vérifie le montant
        if montant <= 0:
            await interaction.response.send_message(
                "❌ Le montant doit être supérieur à 0.",
                ephemeral=True
            )
            return

        # Effectue le transfert
        succes, message = db_payer_joueur(
            interaction.user.id,
            joueur.id,
            montant
        )

        if not succes:
            await interaction.response.send_message(
                f"❌ {message}",
                ephemeral=True
            )
            return

        # Confirme le paiement
        await interaction.response.send_message(
            f"💸 **Transfert effectué !**\n\n"
            f"👤 Expéditeur : {interaction.user.mention}\n"
            f"🎁 Destinataire : {joueur.mention}\n"
            f"💰 Montant envoyé : **{montant}** Pokédollars"
        )


    @bot.tree.command(
        name="ajouter_argent",
        description="Ajouter de l'argent à un joueur"
    )
    @app_commands.describe(
        joueur="Le joueur qui recevra l'argent",
        montant="Le montant à ajouter"
    )
    async def ajouter_argent(
        interaction: discord.Interaction,
        joueur: discord.Member,
        montant: int
    ):

        # Vérifie les permissions
        if not est_admin(interaction):
            await interaction.response.send_message(
                "❌ Tu dois être administrateur "
                "ou posséder le rôle autorisé "
                "pour utiliser cette commande.",
                ephemeral=True
            )
            return

        # Vérifie que le montant est valide
        if montant <= 0:
            await interaction.response.send_message(
                "❌ Le montant doit être supérieur à 0.",
                ephemeral=True
            )
            return

        # Ajoute l'argent au joueur
        succes = db_ajouter_argent(
            joueur.id,
            montant
        )

        if not succes:
            await interaction.response.send_message(
                "❌ Ce joueur n'a pas encore "
                "créé son personnage.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"✅ **{montant} Pokédollars** "
            f"ont été ajoutés à {joueur.mention}."
        )


    @bot.tree.command(
        name="retirer_argent",
        description="Retirer de l'argent à un joueur"
    )
    @app_commands.describe(
        joueur="Le joueur à qui retirer l'argent",
        montant="Le montant à retirer"
    )
    async def retirer_argent(
        interaction: discord.Interaction,
        joueur: discord.Member,
        montant: int
    ):

        # Vérifie les permissions
        if not est_admin(interaction):
            await interaction.response.send_message(
                "❌ Tu dois être administrateur "
                "ou posséder le rôle autorisé "
                "pour utiliser cette commande.",
                ephemeral=True
            )
            return

        # Vérifie que le montant est valide
        if montant <= 0:
            await interaction.response.send_message(
                "❌ Le montant doit être supérieur à 0.",
                ephemeral=True
            )
            return

        # Retire l'argent du joueur
        succes = db_retirer_argent(
            joueur.id,
            montant
        )

        if not succes:
            await interaction.response.send_message(
                f"❌ {joueur.mention} n'a pas suffisamment "
                f"de Pokédollars ou n'a pas encore "
                f"créé son personnage.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"✅ **{montant} Pokédollars** "
            f"ont été retirés à {joueur.mention}."
        )