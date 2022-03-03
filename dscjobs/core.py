import datetime
from typing import Iterable
import aiohttp
import asyncio
from .exceptions import *

class Session:
    def __init__(self,**tmp):
        self.session = tmp

class ClientSession:
    def __init__(self,**kwargs):
        self.optnal = kwargs
        self.onces = []
        self.config = {}

    async def _runner(self,function):
        await function()
        exit()

    def once(self,coro):
        """Execute a new Coroutine. Use this instead of asyncio.run()ing a function

        Args:
            coro (asyncio.Coroutine)

        Raises:
            MalformedRequest
            UserNotFound
            NoReviewAvailable

        Returns:
            once.handle()
        """
        self.config['MAIN_COROUTINE'] = coro
        def handle(func):
            return 0

        return handle

    def run(self):
        if 'MAIN_COROUTINE' in self.config:
            func = self.config['MAIN_COROUTINE']
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self._runner(func))
            
            exit()
        else:
            raise DSCJobsBaseException("No ClientSession.config['MAIN_COROUTINE'] was set. Use @ClientSession.once instead.")

    def find(self,predicate,seq:Iterable):
        """A helper to return the first element found in the sequence
        that meets the predicate. For example: ::
            member = ClientSession.find(lambda m: m.id == 899722893603274793, PeopleThatVotedForMe)
        would find the first :class:`~dscjobs.User` whose ID is 899722893603274793 and return it.
        If an entry is not found, then ``None`` is returned.
        This is different from :func:`py:filter` due to the fact it stops the moment it finds
        a valid entry.
        Parameters
        -----------
        predicate
            A function that returns a boolean-like result. (e.G. lambda m: m.id==899722893603274793)
        seq: :class:`typing.Iterable`
            The iterable to search through.
        
        """
        for item in seq:
            if predicate(item):
                return item
        return None

class Review:
    def __init__(self,user,content,likes,dislikes,reports,replies,rate,date):
        self.user = user
        self.content = content
        self.likes = likes
        self.dislikes = dislikes
        self.reports = reports
        self.replies = replies
        self.date = date
        self.rate = rate



class User:
    def __init__(self,id,banned,staff,premium,lifetime, created_at,**other):
    
        """ Generates a User Object. Do not use directly, use fetchUser() instead
    
        :int id:
        :param id:
    
        :type banned:
        :param banned:
    
        :type staff:
        :param staff:
    
        :type premium:
        :param premium:
    
        :type lifetime:
        :param lifetime:
    
        :type created_at:
        :param created_at:
    
        :type **other:
        :param **other:
    
        :raises:
    
        :rtype:
        """    
        
        self.id = id
        self.banned = banned
        self.staff = staff
        self.premium = premium
        self.lifetime = lifetime
        self.created_at = created_at#datetime.datetime.fromtimestamp(int(created_at))
        

async def fetchUser(userid,**context):
    async with aiohttp.ClientSession() as cs:
        resp = await cs.get(f'https://api.dscjobs.org/user/{userid}')
        resp.raise_for_status()
        data = await resp.json()
        if "error" in data:
            if resp.status == 400:
                raise MalformedRequest(userid,context)
            if resp.status == 404:
                raise UserNotFound(userid,context)
        data['created_at'] = data['duration']
        data['id'] = data['userID']
        resp.close()
        return User(data['id'],data['banned'],data['staff'],data['premium'],data['lifetime'],data['duration'])

async def fetchReview(userid):
    async with aiohttp.ClientSession() as cs:
        resp = await cs.get(f'https://api.dscjobs.org/rev/{userid}')
        data = await resp.json()
        if "error" in data:
            if resp.status == 400:
                raise UserNotFound(userid)
            if resp.status == 404:
                raise NoReviewAvailable(userid)
        Reviewer = await fetchUser(data['userID'])
        rev = Review(Reviewer,data['content'],data['likes'],data['dislikes'],data['reports'],data['replies'],data['rate'],data['date'])
        rev._review_id = data['_id']
        return rev
