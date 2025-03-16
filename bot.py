import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

class BotData:
    def __init__(self):
        self.welcome_channel = None
        self.goodbye_channel = None

        self.reaction_role = None
        self.reaction_message = None

botdata = BotData()
@bot.event
async def on_ready():
    print("Your bot is ready.")

# REPLY COMMAND

@bot.event
async def on_message(message):
    # Prevent the bot from replying to itself
    if message.author == bot.user:
        return

    # Check if the message contains "x"
    if message.content.lower() == "lenny":
        await message.channel.send("yes lenny is the queen")

    # Required to process other commands
    await bot.process_commands(message)

# SAY COMMAND !say #chat

@bot.command()
async def say(ctx, channel: discord.TextChannel, *, message):
    # Check if the user has permissions (optional)
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("You don't have permission to use this command!")
        return

    await channel.send(message)  # Send the message to the specified channel
    await ctx.send(f"Message sent to {channel.mention}!")  # Confirm message was sent

import asyncio

# DOX COMMAND

@bot.command()
async def dox(ctx, member: discord.Member):
    msg = await ctx.send(f"doxing {member.name}...")
    await asyncio.sleep(2)
    await ctx.send(content="Password Roblox found: `1hwaunt3d@ys`")
    await asyncio.sleep(2)
    await ctx.send(content="IP Address: `192.168.1.1`")
    await asyncio.sleep(2)
    await ctx.send(content="Country: Nigerea")

# PURGE ALL CHANNELS !deletechannels

@bot.command()
@commands.has_permissions(administrator=True)
async def deletechannels(ctx):
    await ctx.send("⚠️ Are you sure you want to delete ALL channels? Type `x` to proceed.")

    def check(m):
        return m.author == ctx.author and m.content == "x"

    try:
        await bot.wait_for("message", check=check, timeout=10)  # Wait 10 sec for confirmation
        for channel in ctx.guild.channels:
            await channel.delete()
        await ctx.send("All channels have been deleted!")
    except asyncio.TimeoutError:
        await ctx.send("Cancelled. No confirmation received.")

# channel create bot !create 10 LAST4LENNY

@bot.command()
@commands.has_permissions(administrator=True)
async def create(ctx, amount: int, *, name: str):
    if amount > 50:  # Prevent excessive spam
        await ctx.send("You can create a maximum of 50 channels at once.")
        return

    for i in range(amount):
        await ctx.guild.create_text_channel(f"{name}-{i+1}")

    await ctx.send(f"Created {amount} channels named '{name}'!")

# mass ping !massping inv

@bot.command()
@commands.has_permissions(administrator=True)
async def massping(ctx, invite: str, times: int):
    if times > 20:  # Limit max pings per channel to 20
        await ctx.send("You can't ping more than 20. To avoid rate limits we can only ping 20 times per channel!")
        return

    message = f"@everyone 🚨 **JOIN THE NEW SERVER!** 🚨\n🔗 {invite}"

    for channel in ctx.guild.text_channels:
        for _ in range(times):
            try:
                await channel.send(message)
                await asyncio.sleep(1)  # Small delay to avoid instant spam
            except discord.Forbidden:
                await ctx.send(f"❌ No permission to send messages in {channel.name}")
                break
            except discord.HTTPException:
                await ctx.send(f"⚠️ Failed to send message in {channel.name}")
                break

    await ctx.send("✅ Mass ping spam completed!")



# mass dm command V2 !massdm

@bot.command()
@commands.has_permissions(administrator=True)
async def massdm(ctx, *, message):
    await ctx.send("Starting mass DM... This may take a while!")

    success = 0
    failed = 0

    for member in ctx.guild.members:
        if member.bot:  # Skip bots
            continue
        try:
            await member.send(message)
            success += 1
            await asyncio.sleep(2)  # Prevent hitting Discord rate limits
        except:
            failed += 1  # Count failed DMs

    await ctx.send(f"Done! Sent to {success} members. Failed: {failed}.")

# delete messages command

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    if amount <= 0:
        await ctx.send("Enter a number greater than 0.")
        return

    def not_pinned(msg):
        return not msg.pinned  # Only delete messages that are NOT pinned

    deleted = await ctx.channel.purge(limit=amount, check=not_pinned)
    await ctx.send(f"Deleted {len(deleted)} messages (excluding pinned ones).", delete_after=5)


# give user full perms

@bot.command()
@commands.has_permissions(administrator=True)
async def give(ctx, member: discord.Member, permission: str):
    if permission.lower() != "full":
        await ctx.send("❌ Invalid permission type. Use `!give @user full`.")
        return

    role_name = "Full Admin"  # Change this if you want a different name

    # Check if role already exists
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    
    # If role doesn't exist, create it with Admin permissions
    if role is None:
        try:
            role = await ctx.guild.create_role(
                name=role_name, 
                permissions=discord.Permissions(administrator=True),
                color=discord.Color.red()
            )
        except discord.Forbidden:
            await ctx.send("I don't have permission to create roles.")
            return

    # Give the role to the user
    try:
        await member.add_roles(role)
        await ctx.send(f"{member.mention} has been granted **full admin** access!")
    except discord.Forbidden:
        await ctx.send("I don't have permission to assign roles.")


# MASS DM COMMAND

@bot.command()
async def dm_all(ctx, *, args=None):
    if args != None:
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(args)
                print("'" + args + "' sent to: " + member.name)

            except:
                print("Couldn't send '" + args + "' to: " + member.name)

    else:
        await ctx.channel.send("A message was not provided.")

bot.run ("discord_token")