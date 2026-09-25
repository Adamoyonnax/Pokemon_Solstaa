
import discord

# Boutons du /pokedex 
class PokemonListeView(discord.ui.View):

    def __init__(self, pokemons, par_page=10):
        super().__init__(timeout=120)

        self.pokemons = pokemons
        self.par_page = par_page
        self.page = 0

        self.nombre_pages = (
            len(pokemons) + par_page - 1
        ) // par_page

        self.mettre_a_jour_boutons()

    def creer_embed(self):

        debut = self.page * self.par_page
        fin = debut + self.par_page

        pokemons_page = self.pokemons[debut:fin]

        description = ""

        for p in pokemons_page:

            symboles = ""

            if p["shiny"] == 1:
                symboles += " ✨"

            if p["talent_cache"] == 1:
                symboles += " 🔮"

            description += (
                f"#{p['id']} {p['name']}{symboles}\n"
            )

        embed = discord.Embed(
            title="🎒 Tes Pokémon",
            description=description,
            color=discord.Color.blue()
        )

        embed.set_footer(
            text=f"Page {self.page + 1}/{self.nombre_pages}"
        )

        return embed

    def mettre_a_jour_boutons(self):

        self.precedent.disabled = self.page == 0
        self.suivant.disabled = (
            self.page >= self.nombre_pages - 1
        )

    @discord.ui.button(
        label="⬅️",
        style=discord.ButtonStyle.secondary
    )
    async def precedent(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        self.page -= 1

        self.mettre_a_jour_boutons()

        await interaction.response.edit_message(
            embed=self.creer_embed(),
            view=self
        )

    @discord.ui.button(
        label="➡️",
        style=discord.ButtonStyle.secondary
    )
    async def suivant(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        self.page += 1

        self.mettre_a_jour_boutons()

        await interaction.response.edit_message(
            embed=self.creer_embed(),
            view=self
        )

    async def on_timeout(self):

        for item in self.children:
            item.disabled = True

        if self.message:
            await self.message.edit(view=self)
            
