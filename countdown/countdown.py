from discord.ext import commands
import asyncio
import calendar
import time

class countdown:
    """Countdown timer!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def countdown(self, ctx, seconds, *, title):
        counter = 0
        try:
            secondint = int(seconds)
            finish = getEpoch(secondint)
            if secondint < 0 or secondint == 0:
                await self.bot.say("I dont think im allowed to do negatives \U0001f914")
                raise BaseException

            message = await self.bot.say("```css" + "\n" + "[" + title +"]" + "\nTimer: " + remaining(finish)[0] + "```")
            while True:
                timer, done = remaining(finish)
                if done:
                    await self.bot.edit_message(message, new_content=("```Ended!```"))
                    break
                await self.bot.edit_message(message, new_content=("```css" + "\n" + "[" + title + "]" + "\nTimer: {0}```".format(timer)))
                await asyncio.sleep(1)
            await self.bot.send_message(ctx.message.channel, ctx.message.author.mention + " Your countdown " + "[" + title + "]"  + " Has ended!")
        except ValueError:
            await self.bot.say("Must be a number!")

def setup(bot):
    n = countdown(bot)
    bot.add_cog(n)

def remaining(epoch):
    remaining = epoch - time.time()
    finish = (remaining < 0)
    m, s = divmod(remaining, 60)
    h, m = divmod(m, 60)
    s = int(s)
    m = int(m)
    h = int(h)
    out = "{:01d}:{:02d}:{:02d}".format(h, m, s)
    return out, finish

def getEpoch(seconds : int):
    epoch = time.time()
    epoch += seconds
    return epoch
