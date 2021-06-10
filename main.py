import discord
import asyncio
from private_data import *
from discord.ext import commands
from discord.member import Member

default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix='-', intents=default_intents)

@bot.event
async def on_ready(): 
    print ("Starting up")
    await bot.change_presence(activity=discord.Game('Axie Infinity'))
    print("Operational")

# COMMANDS FOR STAFF
@bot.command(name='scholar', help="This command gives the role \"Scholar\" and send a DM with all the informations needed. [!scholar][@member]")
async def setup_scholar(ctx, *members: Member):
    if admin_role.lower() in [role.name.lower() for role in ctx.author.roles]:
        if not members: #If "members" tuple is empty
            await ctx.send('Please, select someone you want to promote as a scholar.')
            return
        else:
            for member in members:
                if scholar_role.lower() in [role.name.lower() for role in member.roles]:
                    await ctx.send('One of the person you\'re trying to promote is already a scholar.')
                    return
                else:
                    general_channel = bot.get_channel(general_channel_id)
                    role = discord.utils.get(ctx.guild.roles, name=scholar_role)
                    await member.add_roles(role)
                    await general_channel.send(f"Congratulations {member.mention} 🎉! You have been chosen as a new scholar ! Please, go check your DM's.")
                    await member.create_dm()
                    await member.send(f"Congratulations {member.mention} 🎉! You have been chosen as a new scholar !")

    else:
        await ctx.send("You don't have the permission to use this command !")

    await discord.Message.delete(ctx.message)

# EVENTS
@bot.event
async def on_member_join():

    # MEMBER COUNTER
    channel = bot.get_channel(stat_channel_id)
    guild = bot.get_guild(guild_id)
    while True:
        await channel.edit(name=f"members {guild.member_count}")

@bot.event
async def on_member_remove():

    # MEMBER COUNTER
    channel = bot.get_channel(stat_channel_id)
    guild = bot.get_guild(guild_id)
    while True:
        await channel.edit(name=f"members {guild.member_count}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message_content = message.content.lower()
    messages_words = message_content.split(' ' or ',')
    if len(messages_words) < 16:
        coffees = ['coffee', 'cofee', 'coffe', 'coffeee', 'kape', 'cafe']
        milks = ['milk', 'gatas', 'leche']
        pingpong = ['ping', 'pong']
        salutations = ['hello', 'hi', 'hey', 'goodmorning', 'goodevening', 'morning', 'goodafternoon', 'goodevening', 'goodnight', 'hai', 'hola']
        congrats = ['congratulation', 'congratulations', 'congrat', 'congrats', 'grats']
        for message_word in messages_words:
            for salutation in salutations:
                if message_word == salutation:
                    await message.add_reaction("👋")
            for coffee in coffees:
                if message_word == coffee:
                    await message.add_reaction("☕")
            for ping in pingpong:
                if message_word == ping:
                    await message.add_reaction("🏓")   
            for milk in milks:
                if message_word == milk:
                    await message.add_reaction("🥛")
            for congrat in congrats:
                if message_word == congrat:
                    await message.add_reaction("🎉")
    
    await bot.process_commands(message)

bot.run(TOKEN)