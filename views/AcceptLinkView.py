import discord
from discord.ui import Button, View

class YesLinkAccount(Button):
    def __init__(self, bot) -> None:
        super().__init__(style=discord.ButtonStyle.success, label="Yes",custom_id="yes_link")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        member = interaction.guild.get_member(interaction.user.id)
        username = self.bot.settings.get(f"Link.Username.{member.id}")
        await member.edit(nick=f"{interaction.user.display_name} ({username})")

        embed = discord.Embed(title="Linked!", description="Your account has been successfully linked.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        channel = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        await channel.send(f"<@{interaction.user.id}> linked their account to {username}")