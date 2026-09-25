import discord
import time
import random

from vue.boutonZone import PokemonView

from database.zones import (
    zone_existe,
    get_pokemons_zone
)

from database.player_pokemon import (
    get_pokemon
)


# Stocke le dernier spawn de chaque joueur
spawn_cooldowns = {}


# Charge la commande /spawn
def charger_commandes_spawn(bot):

    @bot.tree.command(
        name="spawn",
        description="Faire apparaître un Pokémon sauvage"
    )
    async def spawn(interaction: discord.Interaction):

        # Répond immédiatement à Discord
        await interaction.response.defer()

        user_id = interaction.user.id
        maintenant = time.time()

        # Vérifie le cooldown du joueur
        dernier_spawn = spawn_cooldowns.get(user_id)

        if dernier_spawn is not None:

            # Cooldown avant qu'un nouveau pokemon spawn : 300 secondes 
            temps_restant = 300 - (
                maintenant - dernier_spawn
            )

            if temps_restant > 0:

                await interaction.followup.send(
                    f"⏳ Attends encore "
                    f"**{temps_restant:.1f} seconde(s)** "
                    f"avant de faire apparaître "
                    f"un autre Pokémon.",
                    ephemeral=True
                )

                return

        # Vérifie que le salon est une zone
        channel_id = interaction.channel.id

        if not zone_existe(channel_id):

            await interaction.followup.send(
                "❌ Ce salon n'est pas une zone."
            )

            return

        # Récupère les Pokémon de la zone
        pokemons = get_pokemons_zone(
            channel_id
        )

        if not pokemons:

            await interaction.followup.send(
                "❌ Aucun Pokémon configuré dans cette zone."
            )

            return

        # Active le cooldown
        spawn_cooldowns[user_id] = maintenant

        # Choisit un Pokémon selon les chances
        pokemon_ids = [
            p["pokemon_id"]
            for p in pokemons
        ]

        chances = [
            p["chance"]
            for p in pokemons
        ]

        pokemon_id = random.choices(
            pokemon_ids,
            weights=chances,
            k=1
        )[0]

        # Chance d'obtenir un shiny : 1 / 4096
        shiny = (
            random.randint(1, 4096) == 1
        )

        # Chance d'avoir le talent caché : 1 / 100
        talent_cache = (
            random.randint(1, 100) == 1
        )

        # Récupère les informations du Pokémon
        pokemon = get_pokemon(
            pokemon_id
        )

        # Crée les boutons du Pokémon
        view = PokemonView(
            pokemon,
            shiny=shiny,
            talent_cache=talent_cache
        )

        # Crée le message du Pokémon sauvage
        embed = discord.Embed(
            title="🌿 Un Pokémon sauvage apparaît !",
            description=(
                f"#{pokemon['id']} "
                f"{pokemon['name']}"
            )
        )

        # Modifie le titre si le Pokémon est shiny
        if shiny:

            embed.title = (
                "✨ Un Pokémon shiny apparaît ! ✨"
            )

        # Indique si le Pokémon possède le talent caché
        if talent_cache:

            embed.description += (
                "\n🔮 **Talent caché !**"
            )

        # Ajoute l'image du Pokémon
        embed.set_image(
            url=pokemon["image"]
        )

        # Envoie le Pokémon dans le salon
        message = await interaction.followup.send(
            embed=embed,
            view=view,
            wait=True
        )

        # Garde le message pour pouvoir le modifier avec les boutons
        view.message = message