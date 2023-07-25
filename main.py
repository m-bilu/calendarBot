import discord
from discord import app_commands
import config
from discord.ext import commands
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import json





####################################################


## Creating instance of bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


## Creating instance of Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def createCalendarService(token):
    creds = google.oauth2.credentials.Credentials.from_authorized_user_info(token, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service

credentialsFile = 'clientAccess.json'

with open(credentialsFile) as f:
    credentialsJSON = json.load(f)


####################################################

## COMMANDS: 

## Use bot.command() decorator to define commands
# Decorator allows commands to sync up with Discord API on launch
# ctx: context of user
# send: send msgs to evoked channel
@bot.command()
async def Hello(ctx):
    await ctx.send("Hello, I'm your bot!")

@bot.command(name='upcomingEvents')
## upcomingEvents should send a msg in evoked channel, containing
# 
async def upcomingEvents(ctx):
    token = credentialsJSON
    service = createCalendarService(token)

    events=service.events().list(calendarId='primary')
    upcomingEvents = events.get('items', [])

    response='Upcoming Events:\n'
    for event in upcomingEvents:
        start = event['start'].get('dateTime', event['start'].get('date'))
        response += f"- {event['summary']}: {start}\n"

    await ctx.send(response)


####################################################


@bot.tree.command(name='echo')
@app_commands.describe(arg= 'What should I say?')
async def say(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"User {interaction.user.name} said: f{arg}",
                                            ephemeral=True)
    


####################################################

## Event to activate
@bot.event
async def on_ready():
    print(f"Bot is ready: {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

##  When you create a bot using Discord.py and define 
# custom commands using the @bot.command() decorator, 
# these commands are not automatically known to 
# Discord until you explicitly register them.

#####################################################







bot.run(config.BOT_TOKEN)
