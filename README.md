# Scholars Organization - Axie Infinity - Discord bot
This bot will help you to handle your scholars and organize your scholarship with Google Sheets

## Setup
1. Create your own Discord bot with https://discord.com/developers/applications/ (you can set the PDP.png file as a profile picture for your bot)
2. Open the private_data.py file and update it with the informations of your server
3. Install the requiered modules by running : ``pip install -r requirements.txt``
4. Host your bot. main.py file must be defined as the execution file

## Get ID's
To get the ID's asking in the private_data.py file, you must follow the following steps:
1. Activate the developer mode on Discord
2. Right click on the channel
3. Copy ID

## Bot's functions
- By running the command ``-scholar [@member]``, you can add a role to all the users who are mentioned and send them a DM. The bot will ask them their Ronin address, their ID card and a picture of them holding their ID card. All this stuff will be sent in a Google Sheets document.
- By defining a channel 'Statistics', the bot will automatically count how many members are on your server
- The bot will automatically react with an emote to messages as 'congratulations', 'hello', 'coffee', 'milk' or pong

## To do
- [x] Implementing small functions as 'statistics' and 'reacting'
- [ ] Make the bot get new scholar's data
- [ ] Make the bot add this data automatically in a Google Sheets file
- [ ] Add commentaries to all the files
- [ ] Clarify the README.md file

## Help
If you need help or you have suggestions, you can contact me on Discord: Baba#4840
