import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pyimgur
import asyncio
from asyncio.tasks import wait_for
from discord.ext import commands
from discord.member import Member
from private_data import *

# Set up the Google Sheets access
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Set up the intents
default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix='-', intents=default_intents)

# Set up the bot
@bot.event
async def on_ready(): 
    print ("Starting up")
    await bot.change_presence(activity=discord.Game('Axie Infinity'))
    print("Operational")

# SCHOLAR COMMAND
@bot.command(name='scholar', help="This command gives the role \"Scholar\" and send a DM with all the informations needed. Then, it writes all the user's datas in a Google Sheet. [-scholar][@member][@member][...]")
async def setup_scholar(ctx, *members: Member):

    # Get the roles items
    admin_role_item = discord.utils.get(ctx.guild.roles, name=admin_role)
    role = discord.utils.get(ctx.guild.roles, name=scholar_role)

    # Delete the command message
    await discord.Message.delete(ctx.message)
    
    # Check if the message's author is an admin
    if admin_role_item in ctx.message.author.roles:

        # Check if someone is mentioned in the command
        if not members:
            await ctx.send('Please, select someone you want to promote as a scholar.')

        else:
            scholar = ['-', '-', '-', '-'] # Placeholders in the gsheet
            im = pyimgur.Imgur(imgur_client_id) # Connection to the Imgur API

            # Set up datas dictionnaries
            newScholars = {}
            newScholarsData = {}

            # Send congrats messages in the general channel
            for member in members:
                if role in member.roles:
                    await ctx.send(f"{member.mention} is already a scholar.")
                else:
                    general_channel = await bot.fetch_channel(general_channel_id)
                    await member.add_roles(role)
                    await general_channel.send(f"Congratulations {member.mention} 🎉! You have been chosen as a new scholar ! Please, go check your DM's.") # Envoie un message de félicitations dans le channel général
                    await member.send(f"Congratulations {member.mention} 🎉! You have been chosen as a new scholar ! There are still a few steps to complete before you can receive the access to your account. If you have any problems during the process, please go ask on the #scholars-chat channel and we'll be very glad to help you. I remember you that this is an automatic message so it is unless to send other stuff that what is asking to you.\n\nLet's begin ! Could you, please, send me your Ronin wallet address ? Must looks like ``ronin:0000000000000000000000000000000000000000``.") # Envoie un message de félicitations en DM et explique le processus qui va suivre
                    newScholars[member.id] = [False, False, False] # Is ronin's wallet address, idCard, picture
                    newScholarsData[member.id] = ["", "", "", ""] # Include ronin's wallet address, idCard, picture datas
            
            # Check function linked to the "wait_for" function
            def check(message) -> bool:

                # Check if the message has been sent in DM
                return (message.channel.type == discord.ChannelType.private) and (message.author in members)
            
            # Function to stop the loop when everyone has sent all the needed datas
            def done() -> bool:
                for member in newScholars.keys():
                    for value in newScholars[member]:
                        if value == False:
                            return True
                return False

            while done():
                try:
                    answer = await bot.wait_for('message', check=check, timeout=None)
                    member = answer.author

                    # Ask for the Ronin address
                    if newScholars[member.id][0] == False:
                        if not answer.content.startswith('ronin:'):
                            await member.send("Sorry, I don't understand what you mean. Please, just send me your Ronin wallet address and nothing else. It must begin with ``ronin:``")
                        
                        else: 

                            # Update the datas dictionaries
                            ronin = str(answer.content)
                            newScholars[member.id][0] = True
                            newScholarsData[member.id][0] = str(member)
                            newScholarsData[member.id][1] = ronin
                            await member.send("Thank you for sending me your Ronin's wallet address!\nLet's do the next step: can you please send a picture of your identity card? If you don't have it, any other document attesting you identity will be fine. Recto is enough, don't need the verso.")

                    # Ask for the ID card picture
                    elif newScholars[member.id][0] == True and newScholars[member.id][1] == False:
                        if not answer.attachments:
                            await member.send("Sorry, I don't understand what you mean. Please, just send me a picture of your ID card and nothing else. It must be a .png or .jpg file.")
                        else:

                            # Update the datas dictionaries and host images on Imgur
                            attachment = answer.attachments[0]
                            if attachment.filename.endswith('png') or attachment.filename.endswith('jpg') or attachment.filename.endswith('jpeg'): # Vérifie que la pièce jointe est bel et bien une image
                                url = attachment.url
                                uploaded_image = im.upload_image(url = url, title="IDCard")
                                img_url = uploaded_image.link
                                await member.send("Thank you for sending me your ID card! Have courage, we are almost at the end!\nCould you please send me a picture of you holding your ID Card or any other document you sent before?")
                                newScholars[member.id][1] = True
                                newScholarsData[member.id][2] = img_url
                            else:
                                await member.send("Sorry, I don't understand what you mean. Please, just send me a picture of your ID card and nothing else. It must be a .png or .jpg file.")

                    # Ask for a picture of the user holding his ID card
                    elif  newScholars[member.id][0] == True and newScholars[member.id][1] == True and newScholars[member.id][2] == False :
                        if not answer.attachments: 
                            await member.send("Sorry, I don't understand what you mean. Please, just send me a picture of you holding your ID card and nothing else. It must be a .png or .jpg file.")
                        else:

                            # Update the datas dictionaries and host images on Imgur
                            attachment = answer.attachments[0]
                            if attachment.filename.endswith('png') or attachment.filename.endswith('jpg') or attachment.filename.endswith('jpeg'): # Vérifie que la pièce jointe est bel et bien une image
                                url = attachment.url
                                uploaded_image = im.upload_image(url = url, title="HoldingIDCard")
                                img_url = uploaded_image.link
                                await member.send("Thank you! You're beautiful! Glad to know you'll work with you 😉\nThank you very much for taking the time to complete these few steps.\nOne of the staff members will get back to you very soon to give you the access information to your account. Thanks again for being part of our team! ❤️")
                                newScholars[member.id][2] = True
                                newScholarsData[member.id][3] = img_url
                            else:
                                await member.send("Sorry, I don't understand what you mean. Please, just send me a picture of you holding your ID card and nothing else. It must be a .png or .jpg file.")
            
                except any:
                    print("Error")

            # Update the gsheet with all the datas that has been gotten previously
            for member in newScholarsData.keys():
                sheet = client.open(sheet_name).sheet1
                sheet.append_row(scholar)
                data = sheet.get_all_records()
                sheet.update_cell(len(data) + 1, 1, newScholarsData[member][0])
                sheet.update_cell(len(data) + 1, 2, newScholarsData[member][1])
                sheet.update_cell(len(data) + 1, 3, newScholarsData[member][2])
                sheet.update_cell(len(data) + 1, 4, newScholarsData[member][3])
                    
    else:
        await ctx.send("You don't have the permission to use this command !")

# REACT WITH EMOTES
@bot.event
async def on_message(message):

    # Check if the author isn't a bot
    if message.author == bot.user:
        return

    message_content = message.content.lower() # Get the message content
    messages_words = message_content.split(' ' and ',') # Make a list with the different words of the message
    if len(messages_words) < 16: # Check if the message's length is smaller than 16 words

        # Define some words lists
        pingpong = ['ping', 'pong']
        salutations = ['hello', 'hi', 'hey', 'goodmorning', 'goodevening', 'goodeve', 'morning', 'goodafternoon', 'goodevening', 'goodnight', 'hai', 'hola']
        congrats = ['congratulation', 'congratulations', 'congrat', 'congrats', 'grats']

        # Check if one of the higher words is in the message content
        for message_word in messages_words:

            for salutation in salutations:
                if message_word == salutation:
                    await message.add_reaction("👋")

            for ping in pingpong:
                if message_word == ping:
                    await message.add_reaction("🏓") 

            for congrat in congrats:
                if message_word == congrat:
                    await message.add_reaction("🎉")
    
    await bot.process_commands(message)

bot.run(TOKEN)