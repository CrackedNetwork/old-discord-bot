import discord
from discord.ui import Button, View

class DownvotePoll(Button):
    def __init__(self, bot) -> None:
        super().__init__(style=discord.ButtonStyle.danger, label="Downvote",custom_id="downvote", emoji="🔽")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        if self.bot.settings.get(f"Poll.Voted.{interaction.user.id}") == None:
            self.bot.settings.set(f"Poll.Voted.{interaction.user.id}", "0")
            embed = discord.Embed(title="Upvoted!", description="You've downvoted this poll", color=discord.Color.light_gray())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            channel = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
            await channel.send(f"<@{interaction.user.id}> Downvoted A Poll")
        else:
            embed = discord.Embed(title="You've already voted for this !", description="You cannot vote twice.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)