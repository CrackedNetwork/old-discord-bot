import discord
from discord.ui import Button, View

from discord.utils import get

class EnterGiveaway(Button):
    def __init__(self, bot) -> None:
        super().__init__(style=discord.ButtonStyle.success, label="Enter the Giveaway", emoji="🎉")
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
                
        role1 = [get(interaction.guild.roles, id=1141050985603674306), 
        get(interaction.guild.roles, id=1123069290061516890), 
        get(interaction.guild.roles, id=1123069290061516889)
        ]
        
        if (interaction.user.roles in role1):
            self.bot.settings.set(f"Giveaway.Users.{interaction.user.name}.Entries", 0)
            self.bot.settings.set(f"Giveaway.Users.{interaction.user.name}.Entries", self.bot.settings.get(f"Giveaway.{interaction.user.name}.Entries")+2)
            await interaction.response.send_message("You've entered the giveaway (2x) and you will be dmed if you win.", ephemeral=True)
            return
        
        role2 = [get(interaction.guild.roles, id=1123069290438983714), 
        discord.utils.get(interaction.guild.roles, id=1141051132567892088), 
        get(interaction.guild.roles, id=1123069290438983712)
        ]

        if (interaction.user.roles in role2):
            self.bot.settings.set(f"Giveaway.Users.{interaction.user.name}.Entries", 0)
            self.bot.settings.set(f"Giveaway.Users.{interaction.user.name}.Entries", self.bot.settings.get(f"Giveaway.{interaction.user.name}.Entries")+3)
            await interaction.response.send_message("You've entered the giveaway (3x) and you will be dmed if you win.", ephemeral=True)
            return

        else:
            self.bot.settings.set(f"Giveaway.Users.{interaction.user.name}.Entries", 0)
            self.bot.settings.set(f"Giveaway.Users.{interaction.user.name}.Entries", self.bot.settings.get(f"Giveaway.{interaction.user.name}.Entries")+2)                
            await interaction.response.send_message("You've entered the giveaway and you will be dmed if you win.", ephemeral=True)
        