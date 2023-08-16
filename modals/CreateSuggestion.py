import discord
import traceback
from discord.interactions import Interaction
import discord.ui
from discord.ui import View, Button

from views.AcceptSuggestionView import AcceptSuggestion
from views.DenySuggestionView import DenySuggestion
from views.DeleteSuggestionView import DeleteSuggestion

class SuggestionModal(discord.ui.Modal):
    def __init__(self, bot, title="Create a Suggestion", *args, **kwargs):
        self.bot = bot
        super().__init__(
            discord.ui.InputText(
                label="Type",
                placeholder="Client",
                max_length=25,
                style=discord.InputTextStyle.short
            ),
            discord.ui.InputText(
                label="Suggestion",
                placeholder="Your Suggestion",
                max_length=500,
                style=discord.InputTextStyle.long
            ),
            title=title,
            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(description=f"**__Type__** : {self.children[0].value}\n\n\n> {self.children[1].value}\n", color=discord.Color.blurple())
        embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar) # type: ignore
        embed.timestamp = discord.utils.utcnow() # type: ignore
        channel = self.bot.get_channel(self.bot.settings.get("Suggestions.Pending")) # type: ignore
        view = View()
        view.add_item(AcceptSuggestion(bot=self.bot))
        view.add_item(DenySuggestion(bot=self.bot))
        view.add_item(DeleteSuggestion(bot=self.bot))
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message("Suggestion created", ephemeral=True)
        channel = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        await channel.send(f"{interaction.user} sent a suggestion")

    async def on_error(self, error: Exception, interaction: Interaction):
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)
