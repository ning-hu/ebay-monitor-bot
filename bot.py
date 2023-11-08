import json
import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord.ext import tasks

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
WATCHLIST = './watchlist.json'

watchlist = {}
intervals = {}
bot = commands.Bot(command_prefix=!)

@bot.command(pass_context=True, name='register', help='Registers the bot to send new ebay listings to this channel. If a current watchlist exists, then use that unless otherwise specified to start a new one.')
async def register(ctx, use_existing:bool=True):
    global CHANNEL
    
    message = ""
    if not CHANNEL:
        CHANNEL = ctx.channel.id
        message += 'Registered this channel for sending updates'

        if (os.path.exists(WATCHLIST)):
            if (not use_existing):
                message += '\nClearing existing watchlist'
                os.remove(WATCHLIST)
            else:
                message += '\nUsing existing watchlist'
                with open(WATCHLIST) as json_file:
                    watchlist = json.load(json_file)

                    # Pretty print in a code block to the channel
                    message += f'\n```{json.dumps(watchlist, indent=2)}```'

                for name in watchlist:
                    intervals[name] = 0
        else:
            message += '\nNo watchlist found. Creating a new one'
    else:
        CHANNEL = None
        message += 'This channel will no longer be sent updates'
    
    await ctx.message.channel.send(message)

@bot.command(pass_context=True, name='watchlistAdd', help='Add a new item to the watchlist.')
async def watchlistAdd(ctx, name:str='', link:str='', price:int=0, interval:int=60):    
    if (not CHANNEL):
        await ctx.message.channel.send("Please register a channel to send updates to first")

    if (name is ''):
        await ctx.message.channel.send("Please send the name of the item")

    if (link is ''):
        await ctx.message.channel.send("Please send the name of the item")

    if (price is 0):
        await ctx.message.channel.send("Please send the max price to watch")

    watchlist[name] = {
        link: link,
        price: price,
        interval: interval
    }

    intervals[name] = 0

    with open(WATCHLIST, "w") as data_file:
        json.dump(watchlist, data_file)

    await ctx.message.channel.send(f'Watching {name} every {interval} seconds')

@bot.command(pass_context=True, name='watchlistRemove', help='Remove and item from the watchlist.')
async def watchlistRemove(ctx, name:str=''):
    if (name is ''):
        await ctx.message.channel.send("Please send the name of the item to stop watching")

    if (name not in watchlist):
        await ctx.message.channel.send(f'{name} is not in the watchlist')

    del watchlist[name]
    del intervals[name]

    with open(WATCHLIST, "w") as data_file:
        json.dump(watchlist, data_file)
    
    await ctx.message.channel.send(f'No longer watching {name}')

@bot.command(pass_context=True, name='watchlistGet', help='Send the current watchlist.')
async def watchlistGet(ctx, item:bool=True):
    message = f'Current watchlist:\n```{json.dumps(watchlist, indent=2)}```'
    
    await ctx.message.channel.send(message)

@tasks.loop(seconds=10)
async def check_watchlist():
    if (not CHANNEL):
        return

    for name in intervals:
        if (intervals[name] is not 0):
            intervals[name] = abs(intervals[name] - 10)
            continue

        listing = watchlist[name]
        
        # do stuff

        intervals[name] = listing[interval]

    channel = bot.get_channel(CHANNEL) 
    await channel.send(f'{counter}')

check_watchlist.start()