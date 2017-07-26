import discord
from discord.ext import commands
from .utils import checks
import urllib
import urllib.request
import shutil
import zipfile
import os
from .utils.dataIO import dataIO
try:
    import PIL
    from PIL import ImageFont
    from PIL import Image
    from PIL import ImageDraw
    hasPil = True
except:
    hasPil = False

from datetime import datetime

class waitingTitan:
    """Functions for Waking Titan ARG"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True, aliases=['nonew', "check"])
    @checks.mod_or_permissions(manage_server=True)
    async def waiting(self, ctx):
        """Generates a Reminder Image stating that when last something might have happened"""
        image = createImage()
        image.save('data/waitingTitan/temp.png')
        channel = ctx.message.channel
        await self.bot.send_file(channel, 'data/waitingTitan/temp.png')
        os.remove('data/waitingTitan/temp.png')


def check_folders(): # This is how you make your folder that will hold your data for your cog
    if not os.path.exists("data/waitingTitan"): # Checks if it exists first, if it does, then nothing executes
        print("Creating data/waitingTitan folder...")  # You can put what you want here. Prints in console for the owner
        os.makedirs("data/waitingTitan") # This makes the directory


def check_files(): # This is how you check if your file exists and let's you create it
    f = "data/waitingTitan/Codystar-Regular.ttf" # f is the path to the file
    if not os.path.isfile(f):
        print("retrieving Font File...")
        url = "https://fonts.google.com/download?family=Codystar"
        file_name = "data/waitingTitan/Codystar.zip"
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        zip_ref = zipfile.ZipFile("data/waitingTitan/Codystar.zip", 'r')
        zip_ref.extractall("data/waitingTitan")
        zip_ref.close()


def setup(bot):
    check_folders();
    check_files();
    if hasPil:
        bot.add_cog(waitingTitan(bot))
    else:
        print("Install Pillow using pip install Pillow")


def createImage():
    now = datetime.utcnow()
    font = ImageFont.truetype("data/waitingTitan/Codystar-Regular.ttf", 35)
    img = Image.new("RGBA", (500,150), (58,58,58))
    draw = ImageDraw.Draw(img)
    draw.text((25,20), "There Is Nothing New", (255,255,255), font=font)
    draw.text((110,60), "As of {year}-{month:02d}-{day:02d}".format(year=now.year, month=now.month, day=now.day), (255,255,255), font=font)
    draw.text((140,100), "At {hour:02d}:{minute:02d} UTC".format(hour=now.hour, minute=now.minute), (255,255,255), font=font)
    return img
