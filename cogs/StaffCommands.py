import discord

from discord import Interaction
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option

from modals.EmbedCreation import EmbedCreation
from modals.ChangeLog import ChangelogModal
from modals.SendDM import DMEmbedCreation

from views.NewSuggestionView import CreateSuggestion
from views.NewTicketView import CreateTicket

from random import randint

class StaffCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    setup = SlashCommandGroup(name="setup", description="Various Setup Commands")
    embed = SlashCommandGroup(name="embed", description="Various Embed Commands")
    dming = SlashCommandGroup(name="dm", description="Various DMing Commands")
    

    @setup.command(name="suggestions", description="Sets up Suggestions")
    async def setup_suggestions(
        self,
        ctx: discord.ApplicationContext,
        panel: Option(discord.TextChannel, "The Channel to send the \"Create a Suggestion\" Panel"),
        pending: Option(discord.Thread, "The Pending Suggestions Thread"),
        accepted: Option(discord.Thread, "The Accepted Suggestions Thread"),
        denied: Option(discord.Thread, "The Denied Suggestions Thread"),
        deleted: Option(discord.TextChannel, "The Deleted Suggestions Threads")
    ):
        if self.bot.settings.get("Suggestions.Panel") != None: # type: ignore
            try:
                channel = await self.bot.fetch_channel(self.bot.settings.get("Suggestions.Panel")) # type: ignore
                message = await channel.history().find(lambda m: m.author == self.bot.user) # type: ignore
                await message.delete() # type: ignore
            except:
                pass
        
        self.bot.settings.set("Suggestions.Panel", panel.id) # type: ignore
        self.bot.settings.set("Suggestions.Pending", pending.id)
        self.bot.settings.set("Suggestions.Accepted", accepted.id)
        self.bot.settings.set("Suggestions.Denied", denied.id)
        self.bot.settings.set("Suggestions.Deleted", deleted.id)
        embed = discord.Embed(
            title="📢 Welcome to the CrackedNetwork Suggestion System! (Inspired by Hybris!)",
            description="🤔 Have a great idea or suggestion for our server? We'd love to hear it! Our suggestion system makes it easy for you to share your thoughts and for us to manage and track your suggestions effectively."
        )
        embed.add_field(name="🗳️ Submitting a Suggestion", value='- 1. Click on the "Submit a suggestion" button below.\n- 2. A modal will appear, allowing you to provide details about your suggestion.\n- 3. Fill out the form with as much information as possible to help us understand your idea.\n- 4. Hit the "Submit" button to send your suggestion.\n', inline=False)
        embed.add_field(name="📝 Review Process:", value="- Once you've submitted a suggestion, it will be reviewed by our team.\n- Initially, your suggestion will appear in the ⁠<#1130812603426426910> thread for evaluation.\n- Our team will carefully consider your suggestion and provide updates as necessary.\n- If your suggestion is accepted, it will be moved to the ⁠<#1130812755629309965> thread. If your suggestion is not feasible or aligns with our current plans, it will be moved to the <#1130812858523979806> thread.\n\n- We'll keep you updated on the status of your suggestion throughout the process.\n", inline=False)
        embed.add_field(name="📌 Important Reminders:", value="- Ensure your suggestion is constructive and aligns with the goals of our server.\n- Avoid submitting duplicate suggestions. Check the existing suggestions before posting.\n- Be patient! The review process may take some time, but we value your input.\n\n👍 Thank you for taking the time to contribute to the CrackedNetwork community! Your suggestions help us make our products even better. If you have any questions, feel free to ask in the support channel.", inline=False)
        embed.set_footer(text="Inspired from Hybris, https://discord.gg/hybris")
        await panel.send(embed=embed, view=CreateSuggestion(bot=self.bot))
        embed = discord.Embed(title="Setup", description="Suggestion successfully setup")
        embed.add_field(name="Panel Channel", value=panel.mention)
        embed.add_field(name="Pending Channel", value=pending.mention)
        embed.add_field(name="Accepted Channel", value=accepted.mention)
        embed.add_field(name="Denied Channel", value=denied.mention)
        await ctx.respond(embed=embed)

    @setup.command(name="tickets", description="Sets up Tickets")
    @commands.has_permissions(manage_channels=True)
    async def setup_tickets(
        self,
        ctx: discord.ApplicationContext,
        panel: Option(discord.TextChannel, "The Channel to send the \"Create a Ticket\" Panel"),
        ticket: Option(discord.CategoryChannel, "The Category to create the Ticket Channel in") 
    ):
        if self.bot.settings.get("Tickets.Panel") != None: # type: ignore
            try:
                channel = await self.bot.fetch_channel(self.bot.settings.get("Tickets.Panel")) # type: ignore
                message = await channel.history().find(lambda m: m.author == self.bot.user) # type: ignore
                await message.delete() # type: ignore
            except:
                pass
        
        self.bot.settings.set("Tickets.Panel", panel.id) # type: ignore
        self.bot.settings.set("Tickets.Category", ticket.id) # type: ignore
        await panel.send(embed=discord.Embed(title="Open a Ticket !", description="By clicking the button, a ticket will be opened for you."), view=CreateTicket(bot=self.bot))
        embed = discord.Embed(title="Setup", description="Ticket Creator successfully setup")
        embed.add_field(name="Panel Channel", value=panel.mention)
        embed.add_field(name="Ticket Category", value=ticket.mention)
        await ctx.respond(embed=embed)


    @embed.command(name="rules", description="Sends Rules Embed")
    @commands.has_permissions(manage_messages = True)
    async def embedrules(
        self,
        ctx: discord.ApplicationContext,
    ):
        embed1 = discord.Embed(title="CrackedNetwork", description="Welcome to the Official Discord Server of CrackedNetwork Client. We are pleased to have you in our journey :D. Before continuing please read the rules and obey them, any user who breaks the rules is going to face some consequences (that is, ban, mute). NOTE: This Discord Server's Layout is inspired by CrackedNetwork.", color=discord.Color.red())
        embed1.set_footer(icon_url="https://asicalug.netlify.app/storage/CrackedNetwork.png",)
        embed2 = discord.Embed(url="https://discord.gg/Hybris", title="Hybris' Discord", color=discord.Color.red())
        embed3 = discord.Embed(title="", color=discord.Color.red())
        embed3.set_image(url="https://media.discordapp.net/attachments/1120373785967738880/1121014281727639684/CrackedNetwork_Rules.png?width=1040&height=585")
        embed4 = discord.Embed(description="Check out the Rules before Starting Your Journey In our Discord Server - CrackedNetwork", title="", color=discord.Color.red())
        embed5 = discord.Embed(title="", description="Remember, the rules are applied to all the behaviour on the server including Moderators and Staffs. If you See anyone breaking the Rules, report it to any online Staff/Mod.", color=discord.Color.red())
        embed5.add_field(name="Rules", value="* 1. Be Respectful and dont be mean to others :D\n\n* 2. No Spamming\n\n* 3. No Advertising,\n\n* 4. No Threatening\n\n* 5. Dont share any personal information\n\n* 6. Be a good person :D")
        await ctx.send_response(embeds=(embed1, embed2, embed3, embed4, embed5))
    
    @embed.command(name="commmunity_support", description="Sends Rules Embed")
    @commands.has_permissions(manage_messages = True)
    async def embedcommunitysupport(
        self,
        ctx: discord.ApplicationContext,
    ):
        embed1 = discord.Embed(title="Community Support's Basics", description="Please use this to seek support from the community and to avoid disturbing any staff members", color=discord.Color.red())
        embed2 = discord.Embed(title="Before Asking", description="Before asking, please check <#1120369654653788302> to avoid annoying anyone and to keep this channel clean.", color=discord.Color.red())
        embed3 = discord.Embed(color=discord.Color.red())
        embed3.set_image(url="https://r2.e-z.host/17a2b375-7193-4f28-94c4-be10a3e7c1b4/iqzm639w.png")
        embed4 = discord.Embed(title="Rules", description="- 1. Please be respectful to others and don't beg for answers\n- 2. If you REALLY need help and there isn't any members that can help you, create a ticket @ <#1127247280991387710>\n- 3. Don't excessively ping anyone\n- 4. Any rules in <#1120363306725679136> apply in this channel.", color=discord.Color.red())
        embed5 = discord.Embed(description="Thank you for reading and understanding.", color=discord.Color.red())
        await ctx.send(embeds=[embed1, embed2, embed3, embed4, embed5])
        await ctx.response.send_message("Embed Sent", ephemeral=True)

    @embed.command(name="changelog", description="Sends a changelog embed")
    @commands.has_permissions(manage_messages=True)
    async def embedchangelog(
        self,
        interaction: discord.Interaction
    ):
        await interaction.response.send_modal(ChangelogModal(bot=self.bot))

    @embed.command(name="create", description="Sends an embeded text")
    @commands.has_permissions(manage_messages=True)
    async def embedchangelog(
        self,
        interaction: discord.Interaction
    ):
        await interaction.response.send_modal(EmbedCreation(bot=self.bot))

    @setup.command(name="log", description="Sets up a logging channel")
    @commands.has_permissions(manage_channels=True)
    async def setuplog(
        self,
        ctx : discord.ApplicationContext,
        channel: Option(discord.TextChannel, "The Channel to send the logs"),
    ):
        self.bot.settings.set("Logs.Channel", channel.id) # type: ignore
        await ctx.send_response("Log Channel set", ephemeral=True)

    @commands.slash_command(name="warn", description="warn a user")
    @commands.has_permissions(moderate_members=True)
    async def warn(
        self, 
        ctx : discord.ApplicationContext,
        user : Option(discord.Member, "The user to warn"),
        reason : Option(str, "The reason the user has been warned")
    ):
        warns = (self.bot.settings.get(f"Warns.{user.id}") or 0) + 1
        self.bot.settings.set(f"Warns.{user.id}", warns)
        channel = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        member = ctx.guild.get_member(ctx.user.id)
        await ctx.send_response(f"<@{user.id}> has been warned", ephemeral=True)
        embed = discord.Embed(title="Warned", description=f"You've been warned by <@{member.id}> in the CrackedNetwork discord server, you now have `{warns}` warns.")
        embed.add_field(name="Reason", value=f"{reason}")
        await user.send(embed=embed)
        await channel.send(f"<@{user.id}> has been warned by <@{member.id}> for {reason} and has now `{warns}` warns.")

    @commands.slash_command(name="remove_warn", description="remove warn(s) from a user")
    @commands.has_permissions(moderate_members=True)
    async def remove_warn(
        self, 
        ctx : discord.ApplicationContext,
        user : Option(discord.Member, "The user to warn"),
        number : Option(int, "How much warns to remove"),
    ): 
        member = ctx.guild.get_member(ctx.user.id)
        remove_warn = self.bot.settings.get(f"Warns.{user.id}")-number
        self.bot.settings.set(f"Warns.{user.id}", remove_warn)
        warns = self.bot.settings.get(f"Warns.{user.id}")
        channel = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        await ctx.send_response(f"{number} warns have been removed from <@{user.id}>", ephemeral=True)
        embed = discord.Embed(title="Warns Removed", description=f"{number} warns has been removed from your account on the CrackedNetwork discord server, you now have `{warns}` warns.")
        await user.send(embed=embed)
        await channel.send(f"<@{member.id}> has removed {number} warns from <@{user.id}> and has now `{warns}` warns.")


    @commands.slash_command(name="info", description="Check a user's informations")
    @commands.has_permissions(moderate_members=True)
    async def info(
        self,
        ctx : discord.ApplicationContext,
        user : discord.Member,
    ):
        warns = self.bot.settings.get(f"Warns.{user.id}")

        if warns==None:
            embed = discord.Embed(title=f"{user}'s Info", description=f"This is {user}'s information")
            embed.set_author(name=f"{user}", icon_url=user.avatar)
            embed.add_field(name="Warns", value=f"{user} has `0` warns.")
            await ctx.send_response(embed=embed)
        else:
            embed = discord.Embed(title=f"{user}'s Info", description=f"This is {user}'s information")
            embed.set_author(name=f"{user}", icon_url=user.avatar)
            embed.add_field(name="Warns", value=f"{user} has `{warns}` warns.")
            await ctx.send_response(embed=embed)


    @commands.slash_command(name="purge", description="Purges a specific amount of messages")
    @commands.has_permissions(moderate_members=True)
    async def purge(
        self,
        ctx : discord.ApplicationContext,
        amount : Option(int)
    ):
        amount = amount
        embed = discord.Embed(title="Purged", description=f"{amount} message.s have been purged")
        await ctx.channel.purge(limit=amount)
        await ctx.send_response(embed=embed, ephemeral=True)
    
    @dming.command(name="embed", description="Send a Direct Message (DM) To a Specific User")
    @commands.has_permissions(moderate_members=True)
    async def dm_embed(
        self,
        ctx : discord.ApplicationContext,
        member : Option(discord.Member)
    ):
        user = ctx.guild.get_member(ctx.user.id)
        self.bot.settings.set(f"Dm.{user.id}", member.id)
        await ctx.response.send_modal(DMEmbedCreation(bot=self.bot))

    @dming.command(name="message", description="Send a Direct Message (DM) To a Specific User")
    @commands.has_permissions(moderate_members=True)
    async def dm_message(
        self,
        ctx : discord.ApplicationContext,
        member : Option(discord.Member, "member to send the message to"),
        message : Option(str, "Message to send")
    ):
        user = ctx.guild.get_member(ctx.user.id)
        await member.send(f"{message}\n*sent by {user.mention}*")
        await ctx.send_response("DM sent", ephemeral=True)

    @commands.slash_command(name="ban", description="Ban a member")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self, 
        ctx : discord.ApplicationContext,
        member : Option(discord.Member, "member to ban from the guild"),
        reason : Option(str, "Reason The Member Has Been Banned For"),
    ):
        guild = discord.Guild.name
        logs = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        embed = discord.Embed(title="You have been banned !", description=f"You have been banned from {guild}")
        embed.add_field(name="Reason : ", value=f"{reason}")
        embed.set_footer(text="If you think that this was an error please contact `adeebur`, `asicalug` or `leocodes.`.")
        await member.send(embed=embed)
        await member.ban()
        await ctx.response.send_message(f"{member.mention} has been banned.", ephemeral=True)
        await logs.send(f"{member.mention} has been unbanned by {ctx.user.mention}.")

    @commands.slash_command(name="unban", description="unban a specific banned member")
    @commands.has_permissions(ban_members=True)
    async def unban(
        self,
        ctx : discord.ApplicationContext,
        id : Option(str, "The member to unban"),
        reason : Option(str, "Reason to unban the member")
    ):
        id = int(id)
        guild = discord.Guild.name
        user = await self.bot.fetch_user(id)
        logs = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        await ctx.guild.unban(user)
        await ctx.response.send_message(f"{user.mention} has been unbanned.", ephemeral=True)
        await logs.send(f"{user.mention} has unbanned {user.mention}.")

    @commands.slash_command(name="lockdown", description="Lock a channel")
    @commands.has_permissions(manage_channels=True)
    async def lockdown(
        self,
        ctx : discord.ApplicationContext,
    ):
        logs = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(title="Channel Locked", description="This Channel has been locked, please be patient while we fix any issues.", color=discord.Color.yellow())
        embed.set_footer(text="CrackedNetwork Staff.")
        await ctx.send(embed=embed)
        await ctx.send_response("Channel has been locked !", ephemeral=True)
        await logs.send(f"{ctx.user.display_name} locked {ctx.channel.mention}")

    @commands.slash_command(name="unlockdown", description="Unlock a channel")
    @commands.has_permissions(manage_channels=True)
    async def unlockdown(
        self,
        ctx : discord.ApplicationContext,
    ):
        logs = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = discord.Embed(title="Channel Unlocked", description="This Channel has been unlocked.", color=discord.Color.green())
        embed.set_footer(text="CrackedNetwork Staff.")
        await ctx.send(embed=embed)
        await ctx.send_response("Channel has been unlocked !", ephemeral=True)
        await logs.send(f"{ctx.user.display_name} unlocked {ctx.channel.mention}")

    @commands.slash_command(name="close", description="Close a Ticket")
    @commands.has_permissions(manage_messages=True)
    async def close_ticket(
        self,
        ctx : discord.ApplicationContext
    ):
        if "ticket" in ctx.channel.name:
            channel1 = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
            await ctx.send("This Ticket Will be deleted in a few moments.")
            await channel1.send(f"{ctx.user.display_name} has deleted {ctx.channel.name}")
            await ctx.channel.delete()
            await channel1.send(f"{ctx.user.display_name} has deleted {ctx.channel.name}")

    @commands.slash_command(name="add", description="Add a member to a ticket")
    @commands.has_permissions(manage_messages=True)
    async def add_to_ticket(
        self,
        ctx : discord.ApplicationContext,
        member : Option(discord.Member)
    ):
        if "ticket" in ctx.channel.name:
            channel = self.bot.get_channel(ctx.channel.id)
            channel1 = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
                member: discord.PermissionOverwrite(read_messages=True), 
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send_response(f"Added {member.mention}.")
            await channel1.send(f"{ctx.user.display_name} added {member.display_name} in {ctx.channel.mention}.")
            


    #=================================
    #============Errors===============
    #================================= 


    @embedrules.error
    async def embedrules_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @setup_suggestions.error
    async def embedrules_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @setup_tickets.error
    async def embedrules_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @embedchangelog.error
    async def embedrules_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @embedchangelog.error
    async def embedcommunitysupport(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @warn.error
    async def warn_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @remove_warn.error
    async def rmwarn_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)
    
    @info.error
    async def info_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @purge.error
    async def purge_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @dm_message.error
    async def purge_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @dm_embed.error
    async def purge_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)
    
    @ban.error
    async def info_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @unban.error
    async def info_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @lockdown.error
    async def info_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @unlockdown.error
    async def info_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(StaffCommands(bot))