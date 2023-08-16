import discord
import traceback
from discord.interactions import Interaction

class DMEmbedCreation(discord.ui.Modal):
    def __init__(self, bot, title="Send a DM with an embeded text", *args, **kwargs):
        self.bot = bot
        super().__init__(
            discord.ui.InputText(
                label="Title",
                placeholder="DMs",
                max_length=50,
                min_length=0,
                style=discord.InputTextStyle.short,
            ),
            discord.ui.InputText(
                label="Description",
                placeholder="I'd like to DM you for...",
                max_length=4000,
                min_length=0,
                style=discord.InputTextStyle.long,
            ),
            discord.ui.InputText(
                label="Field Title",
                placeholder="Field Title...",
                max_length=100,
                min_length=0,
                style=discord.InputTextStyle.short,
                required=False,
            ),
            discord.ui.InputText(
                label="Field Description",
                placeholder="Field Description...",
                max_length=4000,
                min_length=0,
                style=discord.InputTextStyle.short,
                required=False,
            ),
            title=title,
            *args,
            **kwargs
        )


    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value, color=discord.Color.blurple())
        embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar) # type: ignore
        embed.add_field(name=self.children[2].value, value=self.children[3].value)
        embed.timestamp = discord.utils.utcnow() # type: ignore
        user = interaction.guild.get_member(interaction.user.id)
        member = interaction.guild.get_member(self.bot.settings.get(f"Dm.{user.id}"))
        await member.send(embed=embed)
        await interaction.response.send_message("DM sent", ephemeral=True)

    async def on_error(self, error: Exception, interaction: Interaction):
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)