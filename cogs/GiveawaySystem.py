import discord

from discord import Interaction
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option
from discord.ui import View, Button

from views.EnterGiveawayView import EnterGiveaway

from random import randint

from datetime import datetime, timedelta

import asyncio

class GiveawaySystem(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    @commands.slash_command(name="giveaway", description="This will start a giveaway")
    @commands.has_permissions(administrator=True)
    async def start_giveaway(
        self,
        ctx : discord.ApplicationContext,
        prizetype : Option(str, description="This will be shown in the giveaway signup embed"),
        time : Option(int, description="Time for the giveaway (**IN HOURS**)"),
        prize : Option(str, "This will be dmed to the winner"),
        winners : Option(int, "Number of members that will win the giveaway")
    ):
        dt = datetime.now()
        td = timedelta(hours=time)
        # your calculated date
        my_date = dt + td
        epoch_time=datetime(1970, 1, 1)
        convertion = (my_date - timedelta(hours=2) - epoch_time)
        embed = discord.Embed(title=prizetype, description=f"React with 🎉 to enter this giveaway\nEnds <t:{round(convertion.total_seconds())}:R>")
        embed.add_field(name="Bonus role entries:", value="- <@&1123069290438983714> 3x entries\n- <@&1123069290438983713> 2x entries\n- <@&1141051132567892088> 3x entries\n- <@&1141050985603674306> 2x entries\n- <@&1123069290438983712> 3x entries\n- <@&1123069290438983711> 3x entries\n- <@&1123069290061516890> 2x entries\n- <@&1123069290061516889> 2x entries")
        view = View()
        view.add_item(EnterGiveaway(bot=self.bot))
        await ctx.send(embed=embed,view=view)
        await asyncio.sleep(time*60*60)
    

def setup(bot: commands.Bot):
    bot.add_cog(GiveawaySystem(bot))