
import discord

from database.recompense import effectuer_fouille, effectuer_rencontre_dresseur


# Charge la commande de fouille
def charger_commandes_recompense(bot):

    @bot.tree.command(
        name="fouille",
        description="Fouiller les environs pour trouver une récompense"
    )
    async def fouille(interaction: discord.Interaction):

        # Effectue la fouille
        resultat = effectuer_fouille(interaction.user.id)

        # Vérifie que le joueur possède un profil
        if resultat["status"] == "no_player":
            await interaction.response.send_message(
                "❌ Tu dois d'abord créer un personnage avec /commencer.",
                ephemeral=True
            )
            return

        # Vérifie le délai de recharge
        if resultat["status"] == "cooldown":
            temps = resultat["remaining"]

            heures = temps // 3600
            minutes = (temps % 3600) // 60
            secondes = temps % 60

            await interaction.response.send_message(
                f"⏳ Tu as déjà fouillé récemment !\n"
                f"Tu pourras recommencer dans "
                f"**{heures}h {minutes}min {secondes}s**.",
                ephemeral=True
            )
            return

        recompense = resultat["recompense"]

        # Prépare le résultat de la fouille
        if recompense["type"] == "pokeball":
            titre = "🔴 5 Pokéballs trouvées !"
            description = (
                "Tu as découvert **5 Pokéballs** !\n"
                "Elles ont été ajoutées à ton inventaire."
            )

        elif recompense["type"] == "superball":
            titre = "🔵 3 Superballs trouvées !"
            description = (
                "Tu as découvert **3 Superballs** !\n"
                "Elles ont été ajoutées à ton inventaire."
            )

        elif recompense["type"] == "argent":
            titre = "💰 Des Pokédollars trouvés !"
            description = (
                "Tu as découvert **1 500 Pokédollars** !\n"
                "L'argent a été ajouté à ton compte."
            )

        else:
            rang = recompense["rang"]

            titre = f"🎁 Objet de rang {rang} découvert !"
            description = (
                f"Tu as trouvé un objet de **rang {rang}** !\n\n"
                "Un MJ devra choisir et te remettre cet objet."
            )

        # Crée l'affichage du résultat
        embed = discord.Embed(
            title="⛏️ Résultat de la fouille",
            description=description,
            color=discord.Color.gold()
        )

        embed.set_footer(
            text="Prochaine fouille disponible dans 12 heures."
        )

        await interaction.response.send_message(
            embed=embed
        )

    @bot.tree.command(
        name="rencontre-dresseur",
        description="Rencontrer un dresseur et gagner des Pokédollars"
    )
    async def rencontre_dresseur(
        interaction: discord.Interaction
    ):

        # Effectue la rencontre
        resultat = effectuer_rencontre_dresseur(
            interaction.user.id
        )

        # Vérifie que le joueur possède un profil
        if resultat["status"] == "no_player":
            await interaction.response.send_message(
                "❌ Tu dois d'abord créer un personnage avec /commencer.",
                ephemeral=True
            )
            return

        # Vérifie le cooldown
        if resultat["status"] == "cooldown":
            temps = resultat["remaining"]

            heures = temps // 3600
            minutes = (temps % 3600) // 60
            secondes = temps % 60

            await interaction.response.send_message(
                f"⏳ Tu as déjà rencontré un dresseur récemment !\n"
                f"Tu pourras en rencontrer un autre dans "
                f"**{heures}h {minutes}min {secondes}s**.",
                ephemeral=True
            )
            return

        montant = resultat["montant"]

        # Prépare le message de récompense
        embed = discord.Embed(
            title="⚔️ Rencontre avec un dresseur !",
            description=(
                "Tu as affronté un dresseur Pokémon et remporté son défi !\n\n"
                f"💰 **Tu remportes {montant:,} Pokédollars !**"
            ),
            color=discord.Color.gold()
        )

        embed.set_footer(
            text="Tu pourras rencontrer un autre dresseur dans 23 heures."
        )

        await interaction.response.send_message(
            embed=embed
        )


