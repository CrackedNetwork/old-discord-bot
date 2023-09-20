import discord
import traceback
from discord.interactions import Interaction
import discord.guild
from discord.ui import View, Button

from views.CloseTicketView import CloseTicket

class CreateTicket(discord.ui.View):
    def __init__(self, bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Create a Ticket", style=discord.ButtonStyle.primary, custom_id="create_ticket", emoji="📩")
    async def button_callback(self, button, interaction: discord.Interaction):
        
        overwrites = {
             interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
             interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
             interaction.user: discord.PermissionOverwrite(read_messages=True), 
        }
        ticket_count_before=self.bot.settings.get("Tickets.Count")
        self.bot.settings.set("Tickets.Count", int(ticket_count_before+1))
        ticket_count_after=self.bot.settings.get("Tickets.Count")
        embed = discord.Embed(description="Thank you for contacting support. Please describe your issue and wait for a staff member to respond.\n **Do NOT ping them.**", color=discord.Color.red())
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=self.bot.settings.get("Tickets.Category"))
        channel = await guild.create_text_channel(name=f"ticket-{ticket_count_after}-{interaction.user.display_name}", category=category, overwrites=overwrites)
        await channel.edit(sync_permissions=True)
        await channel.send(f"{interaction.user.mention} Welcome!",embed=embed, view=CloseTicket(bot=self.bot))
        self.bot.settings.set(f"Tickets.UserChannel.{interaction.user.id}", channel.id) # type: ignore
        channel1 = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        await channel1.send(f"{interaction.user} Created a ticket")
        await interaction.response.send_message("Ticket Created", ephemeral=True)

    async def on_error(self, error: Exception, interaction: Interaction):
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)


