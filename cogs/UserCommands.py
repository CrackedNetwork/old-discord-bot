from discord.ext import commands
import discord
from discord.commands import Option
from discord.ui import View, Button
 
from views.AcceptLinkView import YesLinkAccount
from views.DenyLinkView import NoLinkAccount

from mojang import API
api = API()

class UserCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")
    
    @commands.slash_command()
    async def ping(self, ctx: discord.ApplicationCommand):
        embed = discord.Embed(title='Pong !', description=f"{self.bot.latency * 1000}ms")
        await ctx.response.send_message(embed=embed)

    @commands.slash_command()
    async def link(
        self,
        ctx: discord.ApplicationCommand,
        username : Option(str)
    ):
        uuid = api.get_uuid(f"{username}")
        member = ctx.guild.get_member(ctx.user.id)
        self.bot.settings.set(f"Link.Username.{member.id}", username) # type: ignore
        if not uuid:
            embed = discord.Embed(title="Error !", description="Username doesn't exist.\n*Keep in mind that this doesn't work with cracked accounts*")
            await ctx.send_response(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title='Is This You ?', description='Confirm that this Minecraft account belongs to you.', color=discord.Color.yellow())
            embed.add_field(name="Minecraft Username", value=f"{username}")
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/128/{uuid}")
            view = View()
            view.add_item(YesLinkAccount(bot=self.bot))
            view.add_item(NoLinkAccount(bot=self.bot))
            await ctx.send_response(embed=embed, view=view, ephemeral=True)


    @commands.slash_command()
    async def unlink(
        self,
        ctx: discord.ApplicationCommand,
    ):
        member = ctx.guild.get_member(ctx.user.id)
        username = self.bot.settings.get(f"Link.Username.{member.id}") # type: ignore
        uuid = api.get_uuid(f"{username}")
        await member.edit(nick=None)
        embed = discord.Embed(title='Account Unlinked !', description='Your Minecraft account has been unlinked', color=discord.Color.yellow())
        embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/128/{uuid}")
        await ctx.send_response(embed=embed, ephemeral=True)
        channel = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        await channel.send(f"<@{ctx.user.id}> unlinked their account ({username})")

    @commands.slash_command()
    async def userinfo(
        self,
        ctx: discord.ApplicationContext,
        member : Option(discord.Member)
    ):
        link = self.bot.settings.get(f"Link.Username.{member.id}")
        uuid = api.get_uuid(f"{link}")
        join = member.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        creation = member.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        discord.Member.display_name
        warns = self.bot.settings.get(f"Warns.{member.id}")
        embed = discord.Embed(title="User Info")
        embed.set_author(name=member.display_name)
        embed.add_field(name="Linked With", value=f"{link}", inline=False)
        embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/128/{uuid}")
        embed.add_field(name="Joined At", value=f"`{join}`", inline=False)
        embed.add_field(name="Created at", value=f"`{creation}`", inline=False)
        if warns==None:
            embed.add_field(name="Warns", value="`0`")
        if warns!=None:
            embed.add_field(name="Warns", value=f"`{warns}`")
        await ctx.send_response(embed=embed, ephemeral=True)

    @commands.slash_command()
    async def serverinfo(
        self,
        ctx: discord.ApplicationContext
    ):
        creation = ctx.guild.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        member_count = ctx.guild.member_count
        roles = [role.mention for role in ctx.guild.roles]
        txt_channels = [channel.mention for channel in ctx.guild.text_channels]
        vc_channels = [channel.mention for channel in ctx.guild.voice_channels]
        categories = [channel.mention for channel in ctx.guild.categories]
        embed = discord.Embed(title=f"ServerInfo ({ctx.guild.name})", description=f"")
        embed.add_field(name="Created at", value=f"{creation}", inline=False)
        embed.add_field(name="Member Count", value=f"{member_count}", inline=False)
        embed.add_field(name="Roles", value=f"{roles}", inline=False)
        embed2 = discord.Embed(title="Text Channels", description=f"{txt_channels}")
        embed2.add_field(name="Voice Channels", value=f"{vc_channels}", inline=False)
        embed2.add_field(name="Categories", value=f"{categories}", inline=False)
        await ctx.send_response(embeds=[embed, embed2], ephemeral=True)
    
    @commands.slash_command()
    async def report(
        self,
        ctx : discord.ApplicationContext,
        username : Option(str),
        reason : Option(str)
    ):
        embed=discord.Embed(title=f"{discord.User.name}'s report", description=f"{username} has been reported for:\n{reason}")
        channel=await self.bot.fetch_channel(1123069291286233137)
        await ctx.send_response("Your report has been sent and a staff member will review it shortly.", ephemeral=True)
        await channel.send(embed=embed)

    @commands.slash_command()
    async def ip(
        self,
        ctx: discord.ApplicationContext,
    ):
        embed = discord.Embed(description="The ip is currently not available. Check <#1123787587052638239> for updates")
        await ctx.send_response(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(UserCommands(bot))