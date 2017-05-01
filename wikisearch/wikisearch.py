from __future__ import print_function, unicode_literals
import discord
from discord.ext import commands
import asyncio
import aiohttp
try:
    from bs4 import BeautifulSoup
    hasSoup = True
except:
    hasSoup = False
import sys
import functools

#note the lack of the command tag, this is on purpose
async def getSummary(terms):
    s =  await summary(terms, sentences=13)
    return s

class wikisearch:
    """Search wikipedia"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def search(self, ctx, *, searchTerms : str):
        """Uses the wikipedia api to search for your search terms."""
        user = ctx.message.author
        try:
            summary, title, url = await getSummary(searchTerms)
        except DisambiguationError as e:
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
                summary, title, url = await getSummary(e.options[0])
            else:
                try:
                    choice = int(response.content)
                except:
                    await self.bot.say("Invalid response. Please try again")
                    return
                if (choice > limit):
                    await self.bot.say("Invalid choice")
                    return
            summary, title, url = await getSummary(e.options[choice-1])
        summary = summary.split("\n")
        summary = summary[0]
        em = discord.Embed(title=title, description="{}\nMore: {}".format(summary,url), colour=0xDEADBF)
        em.set_author(name='Wikipedia', icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Wikipedia-logo-v2-en.svg/1200px-Wikipedia-logo-v2-en.svg.png")
        #if image.lower().endswith(".gifv") or image.lower().endswith(".gif") or image.lower().endswith(".png") or image.lower().endswith(".jpeg") or image.lower().endswith(".jpg"):
        #    em.set_image(url=image[0])
        try:
            await self.bot.say(embed=em)
        except:
            print("Unable to send message {}".format(em))
            await self.bot.say("Search Failed");

    @commands.command()
    async def wikir(self):
        """Uses the wikipedia API to return a random page"""
        randomTitle = await random()
        try:
            summary, title, url = await getSummary(randomTitle)
        except DisambiguationError as e:
            summary, title, url = await getSummary(e.options[0])
        summary = summary.split("\n")
        summary = summary[0]
        em = discord.Embed(title=title, description="{}\nMore: {}".format(summary,url), colour=0xDEADBF)
        em.set_author(name='Wikipedia', icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Wikipedia-logo-v2-en.svg/1200px-Wikipedia-logo-v2-en.svg.png")
        #if image.lower().endswith(".gifv") or image.lower().endswith(".gif") or image.lower().endswith(".png") or image.lower().endswith(".jpeg") or image.lower().endswith(".jpg"):
        #    em.set_image(url=image[0])
        await self.bot.say(embed=em)

def setup(bot):
    if hasSoup:
        bot.add_cog(wikisearch(bot))
    else:
        print("Install BeautifulSoup4 using pip install BeautifulSoup4")

#Define Colours
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#exception Definitions

ODD_ERROR_MESSAGE = "This shouldn't happen. Please report on GitHub: github.com/goldsmith/Wikipedia"


class WikipediaException(Exception):
  """Base Wikipedia exception class."""

  def __init__(self, error):
    self.error = error

  def __unicode__(self):
    return "An unknown error occured: \"{0}\". Please report it on GitHub!".format(self.error)

  if sys.version_info > (3, 0):
    def __str__(self):
      return self.__unicode__()

  else:
    def __str__(self):
      return self.__unicode__().encode('utf8')


class PageError(WikipediaException):
  """Exception raised when no Wikipedia matched a query."""

  def __init__(self, pageid=None, *args):
    if pageid:
      self.pageid = pageid
    else:
      self.title = args[0]

  def __unicode__(self):
    if hasattr(self, 'title'):
      return u"\"{0}\" does not match any pages. Try another query!".format(self.title)
    else:
      return u"Page id \"{0}\" does not match any pages. Try another id!".format(self.pageid)


class DisambiguationError(WikipediaException):
  """
  Exception raised when a page resolves to a Disambiguation page.

  The `options` property contains a list of titles
  of Wikipedia pages that the query may refer to.

  .. note:: `options` does not include titles that do not link to a valid Wikipedia page.
  """

  def __init__(self, title, may_refer_to):
    self.title = title
    self.options = may_refer_to

  def __unicode__(self):
    return u"\"{0}\" may refer to: \n{1}".format(self.title, '\n'.join(self.options))


class RedirectError(WikipediaException):
  """Exception raised when a page title unexpectedly resolves to a redirect."""

  def __init__(self, title):
    self.title = title

  def __unicode__(self):
    return u"\"{0}\" resulted in a redirect. Set the redirect property to True to allow automatic redirects.".format(self.title)


class HTTPTimeoutError(WikipediaException):
  """Exception raised when a request to the Mediawiki servers times out."""

  def __init__(self, query):
    self.query = query

  def __unicode__(self):
    return u"Searching for \"{0}\" resulted in a timeout. Try again in a few seconds, and make sure you have rate limiting set to True.".format(self.query)

#Utility Definitions

def debug(fn):
  def wrapper(*args, **kwargs):
    print(fn.__name__, 'called!')
    print(sorted(args), tuple(sorted(kwargs.items())))
    res = fn(*args, **kwargs)
    print(res)
    return res
  return wrapper


# from http://stackoverflow.com/questions/3627793/best-output-type-and-encoding-practices-for-repr-functions
def stdout_encode(u, default='UTF8'):
  encoding = sys.stdout.encoding or default
  if sys.version_info > (3, 0):
    return u.encode(encoding).decode(encoding)
  return u.encode(encoding)

#Wikipedia API Definitions
API_URL = 'http://en.wikipedia.org/w/api.php'
USER_AGENT = 'wikipedia (https://github.com/goldsmith/Wikipedia/)'

class WikipediaPage(object):
      '''
      Contains data from a Wikipedia page.
      Uses property methods to filter data from the raw HTML.
      '''
      async def create(title=None, pageid=None, redirect=True, preload=False, original_title=''):
          self = WikipediaPage(title, pageid, redirect, preload, original_title)
          await self.__load(redirect=redirect, preload=preload)
          return self

      def __init__(self, title=None, pageid=None, redirect=True, preload=False, original_title=''):
        if title is not None:
          self.title = title
          self.original_title = original_title or title
        elif pageid is not None:
          self.pageid = pageid
        else:
          raise ValueError("Either a title or a pageid must be specified")

        if preload:
          for prop in ('content', 'summary', 'images', 'references', 'links', 'sections'):
            getattr(self, prop)

      def __repr__(self):
        return stdout_encode(u'<WikipediaPage \'{}\'>'.format(self.title))

      def __eq__(self, other):
        try:
          return (
            self.pageid == other.pageid
            and self.title == other.title
            and self.url == other.url
          )
        except:
          return False

      async def __load(self, redirect=True, preload=False):
        '''
        Load basic information from Wikipedia.
        Confirm that page exists and is not a disambiguation/redirect.

        Does not need to be called manually, should be called automatically during __init__.
        '''
        query_params = {
          'prop': 'info|pageprops',
          'inprop': 'url',
          'ppprop': 'disambiguation',
          'redirects': '',
        }
        if not getattr(self, 'pageid', None):
          query_params['titles'] = self.title
        else:
          query_params['pageids'] = self.pageid

        request = await _wiki_request(query_params)

        query = request['query']
        pageid = list(query['pages'].keys())[0]
        page = query['pages'][pageid]

        # missing is present if the page is missing
        if 'missing' in page:
          if hasattr(self, 'title'):
            raise PageError(self.title)
          else:
            raise PageError(pageid=self.pageid)

        # same thing for redirect, except it shows up in query instead of page for
        # whatever silly reason
        elif 'redirects' in query:
          if redirect:
            redirects = query['redirects'][0]

            if 'normalized' in query:
              normalized = query['normalized'][0]
              assert normalized['from'] == self.title, ODD_ERROR_MESSAGE

              from_title = normalized['to']

            else:
              from_title = self.title

            assert redirects['from'] == from_title, ODD_ERROR_MESSAGE

            # change the title and reload the whole object
            await self.create(redirects['to'], redirect=redirect, preload=preload)

          else:
            raise RedirectError(getattr(self, 'title', page['title']))

        # since we only asked for disambiguation in ppprop,
        # if a pageprop is returned,
        # then the page must be a disambiguation page
        elif 'pageprops' in page:
          query_params = {
            'prop': 'revisions',
            'rvprop': 'content',
            'rvparse': '',
            'rvlimit': 1
          }
          if hasattr(self, 'pageid'):
            query_params['pageids'] = self.pageid
          else:
            query_params['titles'] = self.title
          request = await _wiki_request(query_params)
          html = request['query']['pages'][pageid]['revisions'][0]['*']

          lis = BeautifulSoup(html, 'html.parser').find_all('li')
          filtered_lis = [li for li in lis if not 'tocsection' in ''.join(li.get('class', []))]
          may_refer_to = [li.a.get_text() for li in filtered_lis if li.a]

          raise DisambiguationError(getattr(self, 'title', page['title']), may_refer_to)

        else:
          self.pageid = pageid
          self.title = page['title']
          self.url = page['fullurl']

      def __continued_query(self, query_params):
        '''
        Based on https://www.mediawiki.org/wiki/API:Query#Continuing_queries
        '''
        query_params.update(self.__title_query_param)

        last_continue = {}
        prop = query_params.get('prop', None)

        while True:
          params = query_params.copy()
          params.update(last_continue)

          request = _wiki_request(params)

          if 'query' not in request:
            break

          pages = request['query']['pages']
          if 'generator' in query_params:
            for datum in pages.values():  # in python 3.3+: "yield from pages.values()"
              yield datum
          else:
            for datum in pages[self.pageid][prop]:
              yield datum

          if 'continue' not in request:
            break

          last_continue = request['continue']

      @property
      def __title_query_param(self):
        if getattr(self, 'title', None) is not None:
          return {'titles': self.title}
        else:
          return {'pageids': self.pageid}

      def html(self):
        '''
        Get full page HTML.

        .. warning:: This can get pretty slow on long pages.
        '''

        if not getattr(self, '_html', False):
          query_params = {
            'prop': 'revisions',
            'rvprop': 'content',
            'rvlimit': 1,
            'rvparse': '',
            'titles': self.title
          }

          request = _wiki_request(query_params)
          self._html = request['query']['pages'][self.pageid]['revisions'][0]['*']

        return self._html

      @property
      def content(self):
        '''
        Plain text content of the page, excluding images, tables, and other data.
        '''

        if not getattr(self, '_content', False):
          query_params = {
            'prop': 'extracts|revisions',
            'explaintext': '',
            'rvprop': 'ids'
          }
          if not getattr(self, 'title', None) is None:
             query_params['titles'] = self.title
          else:
             query_params['pageids'] = self.pageid
          request = _wiki_request(query_params)
          self._content     = request['query']['pages'][self.pageid]['extract']
          self._revision_id = request['query']['pages'][self.pageid]['revisions'][0]['revid']
          self._parent_id   = request['query']['pages'][self.pageid]['revisions'][0]['parentid']

        return self._content

      @property
      def revision_id(self):
        '''
        Revision ID of the page.

        The revision ID is a number that uniquely identifies the current
        version of the page. It can be used to create the permalink or for
        other direct API calls. See `Help:Page history
        <http://en.wikipedia.org/wiki/Wikipedia:Revision>`_ for more
        information.
        '''

        if not getattr(self, '_revid', False):
          # fetch the content (side effect is loading the revid)
          self.content

        return self._revision_id

      @property
      def parent_id(self):
        '''
        Revision ID of the parent version of the current revision of this
        page. See ``revision_id`` for more information.
        '''

        if not getattr(self, '_parentid', False):
          # fetch the content (side effect is loading the revid)
          self.content

        return self._parent_id

      @property
      async def summary(self):
        '''
        Plain text summary of the page.
        '''

        if not getattr(self, '_summary', False):
          query_params = {
            'prop': 'extracts',
            'explaintext': '',
            'exintro': '',
          }
          if not getattr(self, 'title', None) is None:
             query_params['titles'] = self.title
          else:
             query_params['pageids'] = self.pageid

          request = await _wiki_request(query_params)
          self._summary = request['query']['pages'][self.pageid]['extract']

        return self._summary

      @property
      async def images(self):
        '''
        List of URLs of images on the page.
        '''

        if not getattr(self, '_images', False):
          self._images = [
            page['imageinfo'][0]['url']
            for page in self.__continued_query({
              'generator': 'images',
              'gimlimit': 'max',
              'prop': 'imageinfo',
              'iiprop': 'url',
            })
            if 'imageinfo' in page
          ]

        return await self._images

      @property
      def coordinates(self):
        '''
        Tuple of Decimals in the form of (lat, lon) or None
        '''
        if not getattr(self, '_coordinates', False):
          query_params = {
            'prop': 'coordinates',
            'colimit': 'max',
            'titles': self.title,
          }

          request = _wiki_request(query_params)

          if 'query' in request:
            coordinates = request['query']['pages'][self.pageid]['coordinates']
            self._coordinates = (Decimal(coordinates[0]['lat']), Decimal(coordinates[0]['lon']))
          else:
            self._coordinates = None

        return self._coordinates

      @property
      def references(self):
        '''
        List of URLs of external links on a page.
        May include external links within page that aren't technically cited anywhere.
        '''

        if not getattr(self, '_references', False):
          def add_protocol(url):
            return url if url.startswith('http') else 'http:' + url

          self._references = [
            add_protocol(link['*'])
            for link in self.__continued_query({
              'prop': 'extlinks',
              'ellimit': 'max'
            })
          ]

        return self._references

      @property
      def links(self):
        '''
        List of titles of Wikipedia page links on a page.

        .. note:: Only includes articles from namespace 0, meaning no Category, User talk, or other meta-Wikipedia pages.
        '''

        if not getattr(self, '_links', False):
          self._links = [
            link['title']
            for link in self.__continued_query({
              'prop': 'links',
              'plnamespace': 0,
              'pllimit': 'max'
            })
          ]

        return self._links

      @property
      def categories(self):
        '''
        List of categories of a page.
        '''

        if not getattr(self, '_categories', False):
          self._categories = [re.sub(r'^Category:', '', x) for x in
            [link['title']
            for link in self.__continued_query({
              'prop': 'categories',
              'cllimit': 'max'
            })
          ]]

        return self._categories

      @property
      def sections(self):
        '''
        List of section titles from the table of contents on the page.
        '''

        if not getattr(self, '_sections', False):
          query_params = {
            'action': 'parse',
            'prop': 'sections',
          }
          query_params.update(self.__title_query_param)

          request = _wiki_request(query_params)
          self._sections = [section['line'] for section in request['parse']['sections']]

        return self._sections

      def section(self, section_title):
        '''
        Get the plain text content of a section from `self.sections`.
        Returns None if `section_title` isn't found, otherwise returns a whitespace stripped string.

        This is a convenience method that wraps self.content.

        .. warning:: Calling `section` on a section that has subheadings will NOT return
               the full text of all of the subsections. It only gets the text between
               `section_title` and the next subheading, which is often empty.
        '''

        section = u"== {} ==".format(section_title)
        try:
          index = self.content.index(section) + len(section)
        except ValueError:
          return None

        try:
          next_index = self.content.index("==", index)
        except ValueError:
          next_index = len(self.content)

        return self.content[index:next_index].lstrip("=").strip()

async def page(title=None, pageid=None, auto_suggest=True, redirect=True, preload=False):
       '''
       Get a WikipediaPage object for the page with title `title` or the pageid
       `pageid` (mutually exclusive).

       Keyword arguments:

       * title - the title of the page to load
       * pageid - the numeric pageid of the page to load
       * auto_suggest - let Wikipedia find a valid page title for the query
       * redirect - allow redirection without raising RedirectError
       * preload - load content, summary, images, references, and links during initialization
       '''

       if title is not None:
         if auto_suggest:
           results, suggestion = await search(title, results=1, suggestion=True)
           try:
             title = suggestion or results[0]
           except IndexError:
             # if there is no suggestion or search results, the page doesn't exist
             raise PageError(title)
         return await WikipediaPage.create(title, redirect=redirect, preload=preload)
       elif pageid is not None:
         return await WikipediaPage.create(pageid=pageid, preload=preload)
       else:
         raise ValueError("Either a title or a pageid must be specified")

async def summary(title, sentences=0, chars=0, auto_suggest=True, redirect=True):
        '''
        Plain text summary of the page.

        .. note:: This is a convenience wrapper - auto_suggest and redirect are enabled by default

        Keyword arguments:

        * sentences - if set, return the first `sentences` sentences (can be no greater than 10).
        * chars - if set, return only the first `chars` characters (actual text returned may be slightly longer).
        * auto_suggest - let Wikipedia find a valid page title for the query
        * redirect - allow redirection without raising RedirectError
        '''

        # use auto_suggest and redirect to get the correct article
        # also, use page's error checking to raise DisambiguationError if necessary
        page_info = await page(title, auto_suggest=auto_suggest, redirect=redirect)
        title = page_info.title
        url = page_info.url
        #images = await page_info.images
        pageid = page_info.pageid

        query_params = {
            'prop': 'extracts',
            'explaintext': '',
            'titles': title
        }

        if sentences:
            query_params['exsentences'] = sentences
        elif chars:
            query_params['exchars'] = chars
        else:
            query_params['exintro'] = ''

        request = await _wiki_request(query_params)
        summary = request['query']['pages'][pageid]['extract']

        return summary, title, url

async def search(query, results=10, suggestion=False):
      '''
      Do a Wikipedia search for `query`.

      Keyword arguments:

      * results - the maxmimum number of results returned
      * suggestion - if True, return results and suggestion (if any) in a tuple
      '''

      search_params = {
        'list': 'search',
        'srprop': '',
        'srlimit': results,
        'limit': results,
        'srsearch': query
      }
      if suggestion:
        search_params['srinfo'] = 'suggestion'

      raw_results = await _wiki_request(search_params)

      if 'error' in raw_results:
        if raw_results['error']['info'] in ('HTTP request timed out.', 'Pool queue is full'):
          raise HTTPTimeoutError(query)
        else:
          raise WikipediaException(raw_results['error']['info'])

      search_results = (d['title'] for d in raw_results['query']['search'])

      if suggestion:
        if raw_results['query'].get('searchinfo'):
          return list(search_results), raw_results['query']['searchinfo']['suggestion']
        else:
          return list(search_results), None

      return list(search_results)

async def _wiki_request(params):
      '''
      Make a request to the Wikipedia API using the given search parameters.
      Returns a parsed dict of the JSON response.
      '''
      global USER_AGENT

      params['format'] = 'json'
      if not 'action' in params:
        params['action'] = 'query'

      headers = {
        'User-Agent': USER_AGENT
      }

      async with aiohttp.get(API_URL, params=params, headers=headers) as response:
        r = await response.json()
        #print(bcolors.WARNING + r + bcolors.ENDC)

      return r

async def random(pages=1):
  '''
  Get a list of random Wikipedia article titles.

  .. note:: Random only gets articles from namespace 0, meaning no Category, User talk, or other meta-Wikipedia pages.

  Keyword arguments:

  * pages - the number of random pages returned (max of 10)
  '''
  #http://en.wikipedia.org/w/api.php?action=query&list=random&rnlimit=5000&format=jsonfm
  query_params = {
    'list': 'random',
    'rnnamespace': 0,
    'rnlimit': pages,
  }

  request = await _wiki_request(query_params)
  titles = [page['title'] for page in request['query']['random']]

  if len(titles) == 1:
    return titles[0]

  return titles
