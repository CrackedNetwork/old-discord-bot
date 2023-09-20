import discord
from discord.ui import Button, View

class UpvotePoll(Button):
    def __init__(self, bot) -> None:
        super().__init__(style=discord.ButtonStyle.success, label="Upvote",custom_id="upvote", emoji="🔼")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        if self.bot.settings.get(f"Poll.Voted.{interaction.user.id}") == None:
            self.bot.settings.set(f"Poll.Voted.{interaction.user.id}", "1")
            embed = discord.Embed(title="Upvoted!", description="You've upvoted this poll", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            channel = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
            await channel.send(f"<@{interaction.user.id}> Upvoted A Poll")
        else:
            embed = discord.Embed(title="You've already voted for this !", description="You cannot vote twice.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)