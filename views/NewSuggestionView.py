import discord

from modals.CreateSuggestion import SuggestionModal

class CreateSuggestion(discord.ui.View):
    def __init__(self, bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Submit a Suggestion", style=discord.ButtonStyle.primary, custom_id="create_suggestion", emoji="💡")
    async def button_callback(self, button, interaction):
        if "Suggestions Ban" in [role.name for role in interaction.user.roles]:
            return await interaction.response.send_message("You are banned from creating Suggestions", ephemeral=True)
        await interaction.response.send_modal(SuggestionModal(bot=self.bot))

