import telnetlib
import threading
import discord
import asyncio
import datetime
import os # This is required because you will be creating folders/files
from .utils.dataIO import dataIO  # This is pulled from Twentysix26's utils
from discord.ext import commands

jsonPath = "data/mudclient/settings.json"
maxWaitTime = 0.5

class mudclient:

    def __init__(self, bot):
        self.bot = bot
        self.clients = []
        self.file_path = jsonPath
        self.settings = dataIO.load_json(self.file_path)
        self.prefix = self.settings["interactChar"]

    @commands.command(pass_context = True, aliases = ["connect"])
    async def startConnection(self, ctx):
        user = ctx.message.author
        channel = ctx.message.channel.id
        if not self.clients:
            hasSession = False
        else:
            for client in self.clients:
                if(client.author == user and client.channel == channel.id):
                    hasSession = True
                else
                    hasSession = False

        if(hasSession != True):
            clientThread = client(self.bot, user, channel.id,self.settings["Server"])
            self.clients.append(clientThread)
            clientThread.start()
            await self.bot.say("```Client Started.\nPlease precede all commands with {}\nClose Session with {}EXIT```".format(self.prefix, self.prefix))
        else:
            await self.bot.say("```you already have a client running in this channel, please remeber to close it with {}EXIT```".format(self.prefix))


    @commands.group(pass_context=True)
    @checks.is_owner()
    async def clientsettings(self, ctx):
        """Settings for MUDClient"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @clientsettings.command(name="prefix", pass_context=True)
    async def _prefix(self, ctx, prefix:str):
        """Set the prefix for the MUDClient"""

        self.prefix = prefix
        self.settings['prefix'] = self.prefix
        dataIO.save_json(jsonPath, self.settings)
        await self.bot.say('`Changed client prefix to {} `'.format(self.prefix))

    #get client messages
    async def on_message(self, message):
        #check if user has a client otherwise ignore message
        if not self.clients:
            hasSession = False
        else:
            for client in self.clients:
                if(client.author == message.author and client.channel == message.channel.id):
                    hasSession = True
                    session = client
                else
                    hasSession = False

        if hasSession:

            if not self.prefix:
                check_folder()
                check_file()

            if message.content.startswith(self.prefix)
                command = message.content.split(self.prefix)[1]
                if not command:
                    return

                await session._write(command)
        else:
            return



def setup(bot):
    check_folders() # runs the folder check on setup that way it exists before running the cog
    check_files() # runs the check files function to make sure the files you have exists
    bot.add_cog(mudclient(bot))

def check_folders(): # This is how you make your folder that will hold your data for your cog
    if not os.path.exists("data/mudclient"): # Checks if it exists first, if it does, then nothing executes
        print("Creating data/mudclient folder...")  # You can put what you want here. Prints in console for the owner
        os.makedirs("data/mudclient") # This makes the directory


def check_files(): # This is how you check if your file exists and let's you create it
    system = {"Server" : {"Name" : "telehack", "IP" : "telehack.com"},
                "interactChar" : "#"}
    f = jsonPath # f is the path to the file
    if not dataIO.is_valid_json(f): # Checks if file in the specified path exists
        print("Creating default settings.json...") # Prints in console to let the user know we are making this file
        dataIO.save_json(f, system)


class client():

    def __init__(self, bot, user: discord.User, channel, server):
        self.author = user
        self.channel = channel
        self.bot = bot
        self.session = server["Name"]
        try:
            self.reader, self.writer = asyncio.open_connection(server["IP"], 23)
            self.running = True
        except:
            print "Bad Connection"

    async def start():

        timeSinceLast = 0
        LastTime = datetime.datetime.now
        while True:
            read = await self.reader.readline()
            if not read:
                timeSinceLast = datetime.datetime.now - LastTime
            else:
                LastTime = datetime.datetime.now
            if timeSinceLast >= maxWaitTime:
                embed=discord.Embed(title=self.session, description=read)
                embed.set_author(name=self.user.display_name, icon_url=self.user.avatar_url)
                await self.bot.say(embed=embed)


    async def _write(self, message:str):
        self.writer.write(message)


    def author():
        return self.author
