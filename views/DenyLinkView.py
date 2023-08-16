import discord
from discord.ui import Button, View

class NoLinkAccount(Button):
    def __init__(self, bot) -> None:
        super().__init__(style=discord.ButtonStyle.danger, label="No")
        self.bot = bot
    
    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Please Enter Your Username Next Time!", description="If you want to link your account, please use your username", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)