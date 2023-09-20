import discord

from discord import Interaction
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option

from discord.utils import get

class RoleGiver(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    claim = SlashCommandGroup(name="claim", description="Various Claiming Commands")

    @commands.Cog.listener()
    async def on_message(self, message):
        message_count = self.bot.settings.get(f"Messages.{message.author.id}")
        if message_count==None:
            self.bot.settings.set(f"Messages.{message.author.id}", 0)
        else:
            self.bot.settings.set(f"Messages.{message.author.id}", message_count+1)

    @claim.command(name="role", description="Claim any role that you can claim")
    async def claim_role(self,
        interaction : discord.Interaction
    ):
        embed = discord.Embed(description="Checking Active Roles...", color=discord.Color.yellow())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        discord.utils.get(interaction.guild.roles, name = "Muted")
        if self.bot.settings.get(f"Messages.{interaction.user.id}") >= 50:
            active_role = discord.utils.get(interaction.guild.roles, id=1123069290061516888)
            await interaction.user.edit(roles=active_role)
        if self.bot.settings.get(f"Messages.{interaction.user.id}") >= 100:
            super_active = discord.utils.get(interaction.guild.roles, id=1123069290061516889)
            await interaction.user.edit(roles=super_active)
        if self.bot.settings.get(f"Messages.{interaction.user.id}") >= 250:
            extremely_active = discord.utils.get(interaction.guild.roles, id=1123069290061516890)
            await interaction.user.edit(roles=extremely_active)
        if self.bot.settings.get(f"Messages.{interaction.user.id}") >= 500:
            insanely_active = discord.utils.get(interaction.guild.roles, id=1123069290438983711)
            await interaction.user.edit(roles=insanely_active)
        if self.bot.settings.get(f"Messages.{interaction.user.id}") >= 1000:
            most_active = discord.utils.get(interaction.guild.roles, id=1123069290438983712)
            await interaction.user.edit(roles=most_active)


def setup(bot: commands.Bot):
    bot.add_cog(RoleGiver(bot))