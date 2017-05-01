try:
    import wikipedia
    wiki = True
except:
    wiki = False
import discord
from discord.ext import commands
import asyncio

#note the lack of the command tag, this is on purpose
async def getSummary(terms):
    return wikipedia.summary(terms)

class wikisearch:
    """Search wikipedia"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def search(self, ctx, *, searchTerms):
        """Uses the wikipedia api to search for your search terms."""
        user = ctx.message.author
        try:
            summary = await getSummary(searchTerms)
            title = searchTerms
        except wikipedia.exceptions.DisambiguationError as e:
            await self.bot.say("Multiple results found:")
            x = 1
            limit = 4
            output = "```"
            for option in e.options:
                if(x <= limit):
                    output += "{}. {}\n".format(x, option)
                else:
                    break;
                x = x+1
            output += "```"
            output += "\nPlease use the numbers to indicate your choice"
            await self.bot.say(output)
            response = await self.bot.wait_for_message(timeout=15, author=user)
            if response is None:
                title = e.options[0]
                summary = await getSummary(e.options[0])
            else:
                try:
                    choice = int(response.content)
                except:
                    await self.bot.say("Invalid response. Please try again")
                    return
                if (choice > limit):
                    await self.bot.say("Invalid choice")
                    return
            summary = await getSummary(e.options[choice-1])
            title = e.options[choice-1]
        em = discord.Embed(title=title, description=summary, colour=0xDEADBF)
        em.set_author(name='Wikipedia', icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Wikipedia-logo-v2-en.svg/1200px-Wikipedia-logo-v2-en.svg.png")
        await self.bot.send_message(ctx.message.channel, embed=em)

def setup(bot):
    if wiki:
        bot.add_cog(wikisearch(bot))
    else:
        print("Install wikipedia api using pip install wikipedia")
