import discord
from discord import app_commands
import config
from discord.ext import commands
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import json

## Creating instance of bot
bot = commands.Bot(command_prefix="!", intents=None)


## Creating instance of Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def createCalendarService(token):
    creds = google.oauth2.credentials.Credentials.from_authorized_user_info(token, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service

credentialsFile = 'clientAccess.json'

with open(credentialsFile) as f:
    credentialsJSON = json.load(f)


## COMMANDS: 
@bot.command()
async def Hello(ctx):
    await ctx.send("Hello, I'm your bot!")

@bot.command()
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

## Event to activate
@bot.event
async def on_ready():
    print(f"Bot is ready: {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


####################################################

@bot.tree.command(name='hello')
async def hello(interaction:discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!",
                                            ephemeral=True)


@bot.tree.command(name='echo')
@app_commands.describe(arg= 'What should I say?')
async def say(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"User {interaction.user.name} said: f{arg}",
                                            ephemeral=True)


bot.run(config.BOT_TOKEN)
