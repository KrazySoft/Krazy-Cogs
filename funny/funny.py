import discord
from discord.ext import commands
import asyncio
import aiohttp
import random
try:
    from bs4 import BeautifulSoup
    hasSoup = True
except:
    hasSoup = False

class funny:
    """Get a funny comic"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['funnyx', 'fx'])
    async def xkcd(self):
        """Randomly retrieve and display a comic from xkcd"""
        url = "https://c.xkcd.com/random/comic/" #build the web adress
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser")
            url = response.url
        try:
            titleFinder = soupObject
            ctitle = titleFinder.find("div", id="ctitle")
            title = ctitle.contents[0]
            imgs = soupObject.find_all("img")
            caption = imgs[1]["title"]
            imgurl = "https:{}".format(imgs[1]["src"])
            em = discord.Embed(title=title, description=caption,url=url, colour=0x002eff)
            em.set_image(url=imgurl)
            em.set_author(name='xkcd.com', icon_url="https://xkcd.com/s/0b7742.png")
            await self.bot.say(embed = em)
        except:
            await self.bot.say("Could not load comic")

    @commands.command(aliases=['funnyc', 'fc'])
    async def cnh(self):
        """Randomly retrieve and display a comic from Cyanide and Happiness"""
        url = "http://explosm.net/comics/random" #build the web adress
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser")
            url = response.url
        try:
            imgs = soupObject.find_all("img")
            imgurl = "https:{}".format(imgs[6]["src"])
            em = discord.Embed(title="Cyanide and Happiness",url=url, colour=0xefc62f)
            em.set_image(url=imgurl)
            em.set_author(name='explosm.net', icon_url="http://explosm.net/img/logo.png")
            await self.bot.say(embed = em)
        except:
            await self.bot.say("Could not load comic")

    @commands.command()
    async def funnyr(self):
        """Randomly Retrieves either an xkcd or Cyanide and Happiness comic"""
        random.seed()
        rand = random.randint(0 , 1)
        if(rand == 1):
            url = "http://explosm.net/comics/random" #build the web adress
            async with aiohttp.get(url) as response:
                soupObject = BeautifulSoup(await response.text(), "html.parser")
                url = response.url
            try:
                imgs = soupObject.find_all("img")
                imgurl = "https:{}".format(imgs[6]["src"])
                em = discord.Embed(title="Cyanide and Happiness",url=url, colour=0xefc62f)
                em.set_image(url=imgurl)
                em.set_author(name='explosm.net', icon_url="http://explosm.net/img/logo.png")
                await self.bot.say(embed = em)
            except:
                await self.bot.say("Could not load comic")
        else:
            url = "https://c.xkcd.com/random/comic/" #build the web adress
            async with aiohttp.get(url) as response:
                soupObject = BeautifulSoup(await response.text(), "html.parser")
                url = response.url
            try:
                titleFinder = soupObject
                ctitle = titleFinder.find("div", id="ctitle")
                title = ctitle.contents[0]
                imgs = soupObject.find_all("img")
                caption = imgs[1]["title"]
                imgurl = "https:{}".format(imgs[1]["src"])
                em = discord.Embed(title=title, description=caption,url=url, colour=0x002eff)
                em.set_image(url=imgurl)
                em.set_author(name='xkcd.com', icon_url="https://xkcd.com/s/0b7742.png")
                await self.bot.say(embed = em)
            except:
                await self.bot.say("Could not load comic")


def setup(bot):
    if hasSoup:
        bot.add_cog(funny(bot))
    else:
        print("Install BeautifulSoup4 using pip install BeautifulSoup4")
