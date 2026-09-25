import discord
import random

from database.player_pokemon import ajouter_pokemon_sql, utiliser_pokeball


class PokemonView(discord.ui.View):

    def __init__(self, pokemon, shiny=False, talent_cache=False):
        super().__init__(timeout=60)
        self.pokemon = pokemon
        self.shiny = shiny
        self.talent_cache = talent_cache
        self.message = None

    # ==========================================
    # POKÉ BALL
    # ==========================================

    @discord.ui.button(
        label="🔴 Poké Ball",
        style=discord.ButtonStyle.success
    )
    async def pokeball(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.tenter_capture(
            interaction,
            "pokeball",
            "Poké Ball",
            40
        )

    # ==========================================
    # SUPER BALL
    # ==========================================

    @discord.ui.button(
        label="🔵 Super Ball",
        style=discord.ButtonStyle.primary
    )
    async def superball(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.tenter_capture(
            interaction,
            "superball",
            "Super Ball",
            50
        )

    # ==========================================
    # HYPER BALL
    # ==========================================

    @discord.ui.button(
        label="🟡 Hyper Ball",
        style=discord.ButtonStyle.danger
    )
    async def hyperball(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.tenter_capture(
            interaction,
            "hyperball",
            "Hyper Ball",
            70
        )

    # ==========================================
    # FONCTION DE CAPTURE
    # ==========================================

    async def tenter_capture(
        self,
        interaction: discord.Interaction,
        type_ball,
        nom_ball,
        taux_capture
    ):
        # Répond immédiatement à Discord
        await interaction.response.defer()

        pokemon = self.pokemon

        # Vérifie que le joueur possède la Ball
        # et en consomme une
        utilisee = utiliser_pokeball(
            interaction.user.id,
            type_ball
        )

        if not utilisee:
            await interaction.followup.send(
                f"❌ Tu n'as plus de **{nom_ball}** !",
                ephemeral=True
            )
            return

        # ==========================================
        # TIRAGE DE CAPTURE
        # ==========================================

        chance = random.randint(1, 100)

        if chance <= taux_capture:

            ajouter_pokemon_sql(
                interaction.user.id,
                pokemon["id"],
                self.shiny,
                self.talent_cache
            )

            embed = discord.Embed(
                title="🎉 Capture réussie !",
                description=(
                    f"Tu as capturé "
                    f"**#{pokemon['id']} {pokemon['name']}** !\n\n"
                    f"🎯 Ball utilisée : **{nom_ball}**"
                ),
                color=discord.Color.green()
            )

            if self.shiny:
                embed.description += "\n✨ **Pokémon Shiny !**"

            if self.talent_cache:
                embed.description += "\n🔮 **Talent Caché !**"

            embed.set_image(url=pokemon["image"])

            await interaction.edit_original_response(
                embed=embed,
                view=None
            )

            return

        # ==========================================
        # CAPTURE ÉCHOUÉE
        # ==========================================

        # 20 % de chance que le Pokémon s'enfuie
        fuite = random.randint(1, 100)

        if fuite <= 20:

            embed = discord.Embed(
                title="💨 Le Pokémon s'est échappé !",
                description=(
                    f"**#{pokemon['id']} {pokemon['name']}** "
                    f"a réussi à s'enfuir !\n\n"
                    f"🎯 Ball utilisée : **{nom_ball}**"
                ),
                color=discord.Color.red()
            )

            await interaction.edit_original_response(
                embed=embed,
                view=None
            )

        else:

            # Le Pokémon reste disponible
            embed = discord.Embed(
                title="💥 La capture a échoué !",
                description=(
                    f"**#{pokemon['id']} {pokemon['name']}** "
                    f"a échappé à la **{nom_ball}** !\n\n"
                    f"🔄 Tu peux tenter une nouvelle capture."
                ),
                color=discord.Color.orange()
            )
            embed.set_image(url=pokemon["image"])

            await interaction.edit_original_response(
                embed=embed,
                view=self
            )

    # ==========================================
    # FUITE DU DRESSEUR
    # ==========================================

    @discord.ui.button(
        label="🏃 Fuite",
        style=discord.ButtonStyle.secondary
    )
    async def fuite(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        embed = discord.Embed(
            title="💨 Le dresseur prend la fuite !",
            description=(
                "Le Pokémon sauvage disparaît "
                "dans les hautes herbes..."
            ),
            color=discord.Color.red()
        )

        await interaction.response.edit_message(
            embed=embed,
            view=None
        )

    # ==========================================
    # TIMEOUT
    # ==========================================

    async def on_timeout(self):

        for item in self.children:
            item.disabled = True

        if self.message:
            await self.message.edit(view=self)