import discord
from discord.ui import Button, View

from discord.utils import get

class EnterGiveaway(Button):
    def __init__(self, bot) -> None:
        super().__init__(style=discord.ButtonStyle.success, label="Enter the Giveaway", emoji="🎉")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        mvpplus = role = discord.utils.find(lambda r: r.name == 'MVP+', interaction.message.guild.roles)
        if mvpplus in interaction.user.roles:
            self.bot.settings.set("Giveaway.User", f"interaction.user.id")
            self.bot.settings.set("Giveaway.User", f"interaction.user.id")
            self.bot.settings.set("Giveaway.User", f"interaction.user.id")
