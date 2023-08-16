import discord
import traceback
from discord.interactions import Interaction

class ChangelogModal(discord.ui.Modal):
    def __init__(self, bot, title="Send a Changelog", *args, **kwargs):
        self.bot = bot
        super().__init__(
            discord.ui.InputText(
                label="Type",
                placeholder="Client",
                max_length=10,
                style=discord.InputTextStyle.short
            ),
            discord.ui.InputText(
                label="Change Log",
                placeholder="- New mods\n- Bug Fixes\netc...",
                max_length=4000,
                style=discord.InputTextStyle.long
            ),
            discord.ui.InputText(
                label="Number",
                placeholder="#696",
                max_length=4,
                style=discord.InputTextStyle.short
            ),
            title=title,
            *args,
            **kwargs
        )


    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value, color=discord.Color.blurple())
        embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar) # type: ignore
        embed.timestamp = discord.utils.utcnow() # type: ignore
        embed.set_footer(text=self.children[2].value)
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Changelog Sent", ephemeral=True)
        channel = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        await channel.send(f"{interaction.user} sent a changelog embed in <#{interaction.channel_id}>")

    async def on_error(self, error: Exception, interaction: Interaction):
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)