import discord
from discord.ui import Button, View

class AcceptSuggestion(Button):
    def __init__(self, bot) -> None:
        super().__init__(style=discord.ButtonStyle.success, label="Accept", emoji="✔️", custom_id="accept_sug", )
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        if self.bot.settings.get(f"Suggestions.Buttons.{interaction.message.id}")=="Used":
            await interaction.response.send_message("This Suggestion has already been Handled.", ephemeral=True)
            self.style=discord.ButtonStyle.gray
        
        if interaction.user.guild_permissions.manage_messages:
            message = await interaction.channel.fetch_message(interaction.message.id)
            embed = message.embeds[0]
            embed.set_footer(text=f"Accepted by {interaction.user.display_name}", icon_url=interaction.user.display_avatar)
            embed.colour = discord.Color.green()
            channel = self.bot.get_channel(self.bot.settings.get("Suggestions.Accepted"))
            await channel.send(embed=embed)
            await message.delete(reason="Suggestion Handled")
            await interaction.response.send_message("Suggestion Accepted !", ephemeral=True)
            logs = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
            await logs.send(f"{interaction.user.name} accepted a suggestion")
            self.bot.settings.set(f"Suggestions.Buttons.{interaction.message.id}", "Used")

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You do not have permissions to do that", ephemeral=True)
