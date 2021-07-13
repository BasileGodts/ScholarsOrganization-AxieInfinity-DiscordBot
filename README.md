# Scholars Organization - Axie Infinity - Discord bot
This bot will help you to handle your scholars and organize your scholarship with Google Sheets.

## Setup
1. Create your own Discord bot by following this tutorial: https://discordpy.readthedocs.io/en/stable/discord.html (you can set the PDP.png file as a profile picture for your bot).
2. Install the requiered modules by running: ``pip install -r requirements.txt``.
5. Follow the first step of this tutorial (Google Drive API and Service Accounts): https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
6. In your Google Sheets document, create 4 columns and name it as: "DiscordID", "RoninAddress", "IDCard", "IDCardHolding". /!\ You must respect this sequence /!\
7. Rename your ``client_secret.json`` file as ``creds.json``.
8. Create an account on Imgur: https://imgur.com/.
9. Go to the following URL, name your application as you want, choose ``OAuth 2 authorization without a callback URL``, enter your email, fill the captcha and click on submit: https://api.imgur.com/oauth2/addclient.
10. Copy your Client ID and paste it in the right field in the ``private_data.py`` file. Don't care about your secret ID.
11. Open the ``private_data.py`` file and update it with information from your own server (in order to have access to the channel IDs, the developer mode must be activated on your Discord account)
12. Host your bot. main.py file must be defined as the execution file.

## Bot's functions
- By running the command ``-scholar [@member][@member][...]``, you can add a role to all the users who are mentioned and send them a DM. The bot will ask them their Ronin address, their ID card and a picture of them holding their ID card. All this stuff will be sent in a Google Sheets document.
- The bot will automatically react with an emote to messages as 'congratulations' or 'hello'.

## To do
- [x] Implementing small functions as 'statistics' and 'reacting'
- [x] Make the bot get new scholar's data
- [x] Make the bot add this data automatically in a Google Sheets file
- [x] Add commentaries to all the files
- [x] Clarify the README.md file

## Help
If you need help or have any suggestions, please contact me on Discord: Baba#4840
