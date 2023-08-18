import discord
from discord.ui import Button, View

class EnterGiveaway(Button):
    def __init__(self, bot) -> None:
        super().__init__(style=discord.ButtonStyle.success, label="Enter the Giveaway", emoji="🎉")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        self.bot.settings.set("Giveaway.Users", interaction.user.id)
        self.bt.settings.set("Giveaway.Entres", self.bot.settings.get("Giveaway.Entries")+1)
        await interaction.response.send_message("You've entered the giveaway and you will be dmed if you win.", ephemeral=True)