import os
from app import keep_alive

import discord
from discord.ext import commands
from dotenv import load_dotenv
from scraper import *
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#keep_alive()

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.wait_until_ready()
    user = client.get_user(656620638869651469)
    user.send("HOE")

"""terms = {
            'F' : 'Fall',
            'W' : 'Winter', 
            'S' : 'Summer'
        }
    
values = []
term = []
year = []

while 1:
    driver, transcript_table = load_page()
    change = minervaupdate(values, term, year, transcript_table, terms)
    if change:
        print("Transcript updated!\n")
        send_email()
    else:
        print("No change...\n")
    time.sleep(60)"""
    
client.run(TOKEN)