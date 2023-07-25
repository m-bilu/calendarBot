
import discord
from discord import app_commands
import config
from discord.ext import commands
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import json
from main import bot

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

