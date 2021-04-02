# discord_bot.py 
# Description: Merging a stock_checker for 3080 graphics card with a discord bot for 24/7 operation.
import os
import discord 
import asyncio
import aiohttp
from bs4 import BeautifulSoup 
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv('.env.txt')
#url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440'
url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440'
url2 = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402'
out_of_stock = 'btn btn-disabled btn-lg btn-block add-to-cart-button'
in_stock = 'btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button'
find_a_store = 'btn btn-secondary btn-lg btn-block add-to-cart-button'
headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.13) Gecko/20080401 BonEcho/2.0.0.13"}

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = discord.Client()
bot = commands.Bot(command_prefix='!') 

async def request_page(site):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(site, headers=headers) as r:
            return await r.text()

async def check_availability(check_site):
    response = await request_page(check_site)
    soup = BeautifulSoup(response, 'html.parser')
    in_s = soup.find("button", in_stock)
    out_s = soup.find("button", out_of_stock) 
    if in_s is not None:
        print("Its in stock") 
        return False
    if out_s is not None:
        print("Out of stock")  
        return True
    else:
        return True

async def send_announcement(web_p): 
    while await check_availability(web_p):
        await asyncio.sleep(10) 
    await bot.wait_until_ready() 
    channel = bot.get_channel(800834982624755772)
    await channel.send(url) 

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
 
@bot.command()
async def test(ctx, arg):
    await ctx.send(arg) 
 
bot.loop.create_task(send_announcement(url))
bot.loop.create_task(send_announcement(url2))
keep_alive()
bot.run(TOKEN)  