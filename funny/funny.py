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

    @commands.command(aliases=['funnys', 'fs'])
    async def se(self):
        """Randomly retrieve and display a comic from Safely Endangered"""
        url = "http://www.safelyendangered.com/?random&nocache=1" #build the web adress
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser")
            url = response.url

        imgs = soupObject.find_all("img")
        heading = soupObject.find_all("h2", class_="post-title")
        title = heading[0].contents[0]
        print(title)
        imgurl = imgs[12]["src"]
        print(imgurl)
        em = discord.Embed(title=title, url=url, colour=0x2a2a2b)
        em.set_image(url=imgurl)
        em.set_author(name='safelyendangered.com', icon_url="http://www.safelyendangered.com/wp-content/uploads/2016/01/safely-endangered-comics-1.png")
        print(em)
        await self.bot.say(embed = em)
        #except:
        #    await self.bot.say("Could not load comic")

    @commands.command()
    async def funnyr(self):
        """Randomly Retrieves either an xkcd or Cyanide and Happiness comic"""
        random.seed()
        rand = random.randint(0 , 2)
        if(rand == 0):
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
        elif(rand == 1):
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
        elif(rand == 2):
            url = "http://www.safelyendangered.com/?random&nocache=1" #build the web adress
            async with aiohttp.get(url) as response:
                soupObject = BeautifulSoup(await response.text(), "html.parser")
                url = response.url
            try:
                imgs = soupObject.find_all("img")
                heading = soupObject.find_all("h2", class_="post-title")
                title = heading[0]
                description = soupObject.find_all("p")
                imgurl = imgs[12]["src"]
                em = discord.Embed(title=title, description=description[0].contents, url=url, colour=0x2a2a2b)
                em.set_image(url=imgurl)
                em.set_author(name='safelyendangered.com', icon_url="http://www.safelyendangered.com/wp-content/uploads/2016/01/safely-endangered-comics-1.png")
                await self.bot.say(embed = em)
            except:
                await self.bot.say("Could not load comic")
        else:
            await self.bot.say("Thats odd you shouldn't be seeing this")


def setup(bot):
    if hasSoup:
        bot.add_cog(funny(bot))
    else:
        print("Install BeautifulSoup4 using pip install BeautifulSoup4")
