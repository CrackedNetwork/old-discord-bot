import discord
class CloseTicket(discord.ui.View):
    def __init__(self, bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label=f"Close ticket", style=discord.ButtonStyle.primary, custom_id="close_tickett", emoji="🔒")
    async def button_callback(self, button, interaction: discord.Interaction):
        if interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="Closed!",
                description="The ticket has been successfully closed.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await interaction.channel.delete()
        else:
            embed = discord.Embed(title='Error', description="You do not have permissions to do that !")
            await interaction.response.send_message(embed=embed)
