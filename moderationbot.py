import discord
from discord.ext import commands

PREFIX = '!'  # Change this to your desired prefix

intents = discord.Intents.default()
intents.members = True
intents.presences = True  
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# anybody with manageroles permissions can use you can change eg manage_channels
def has_manage_roles_permission(ctx):
    return ctx.author.guild_permissions.manage_roles

# Command to kick a member
@bot.command()
@commands.check(has_manage_roles_permission)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked.')

# ban command change it to discord id if you want
@bot.command()
@commands.check(has_manage_roles_permission)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned.')

#  unbans from server
@bot.command()
@commands.check(has_manage_roles_permission)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} has been unbanned.')
            return

# purges message
@bot.command()
@commands.check(has_manage_roles_permission)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)

# Command to mute a member
@bot.command()
@commands.check(has_manage_roles_permission)
async def mute(ctx, member: discord.Member):
    # own config here eg what role and what to do
    pass

# Command to unmute a member
@bot.command()
@commands.check(has_manage_roles_permission)
async def unmute(ctx, member: discord.Member):
    # add your own command here eg what role
    pass

# announces with channel id so !announce channel id message
@bot.command()
@commands.check(has_manage_roles_permission)
async def announce(ctx, channel_id: int, *, message):
    channel = bot.get_channel(channel_id)
    await channel.send(message)

# Command to list commands
@bot.command()
@commands.check(has_manage_roles_permission)
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", color=0x00ff00)
    embed.add_field(name="!kick <user> [reason]", value="Kick a user from the server.", inline=False)
    embed.add_field(name="!ban <user> [reason]", value="Ban a user from the server.", inline=False)
    embed.add_field(name="!unban <user#discriminator>", value="Unban a user from the server.", inline=False)
    embed.add_field(name="!purge <amount>", value="Delete a specified number of messages from the channel.", inline=False)
    embed.add_field(name="!mute <user>", value="Mute a user in the server.", inline=False)
    embed.add_field(name="!unmute <user>", value="Unmute a user in the server.", inline=False)
    embed.add_field(name="!announce <channel_id> <message>", value="Send an announcement to a specific channel.", inline=False)
    await ctx.send(embed=embed)

bot.run("token here")
