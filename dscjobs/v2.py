import datetime
from typing import Iterable
import asyncio
from .v1 import fetchReview
import requests
from .exceptions import *
from datetime import datetime as _dt

class Review:
    def __init__(self,user,content,likes,dislikes,reports,replies,rate,date,pending,flagged, allowed):
        self.user = user
        self.content = content
        self.likes = likes
        self.dislikes = dislikes
        self.reports = reports
        self.replies = replies
        self.date = _dt.fromtimestamp(date)
        self.rate = rate
        self.pending = pending
        self.flagged = flagged
        self.allowed = allowed



class User:
    def __init__(self,id,banned,staff,premium,lifetime, created_at,**other):
        """
        The __init__ function is called when a new object is created from the class. 
        The init function can take arguments, but self is always the first one. 
        Self is a reference to the instance of the class. With self., you can access 
        the attributes and methods of the class.
        
        :param self: Used to Reference the object itself.
        :param id: Used to Set the id of the user.
        :param banned: Used to Determine if the user is banned or not.
        :param staff: Used to Indicate whether the user is a moderator or not.
        :param premium: Used to Determine if the user is premium or not.
        :param lifetime: Used to Determine whether the user is a lifetime member or not.
        :param created_at: Used to Set the date when the user was created.
        :param **other: Used to Add any other attributes to the class.
        :return: The object itself.
        """
        
        self.id = id
        self.banned = banned
        self.staff = staff
        self.premium = premium
        self.lifetime = lifetime
        self.created_at = created_at#datetime.datetime.fromtimestamp(int(created_at))


def fetchReview(review_id):
    with requests.get(f'https://api.dscjobs.org/v2/ rev/user/{review_id}') as resp:
        data = resp.json()
        if "error" in data:
            if resp.status == 400:
                raise UserNotFound(review_id)
            if resp.status == 404:
                raise NoReviewAvailable(review_id)
        Reviewer = fetchUser(data['userID'])
        rev = Review(Reviewer,data['content'],data['likes'],data['dislikes'],data['reports'],data['replies'],data['rate'],data['date'],data["pending"],data["flagged"],data["allowed"])
        rev._review_id = data['_id']
        return rev

def fetchReviews(user_id):
    with requests.get(f'https://api.dscjobs.org/rev/all/{user_id}') as resp:
        data = resp.json()
        if "error" in data:
            if resp.status == 400:
                raise DSCJobsBaseException(user_id)
            if resp.status == 404:
                raise UserNotFound(user_id)
        lst = []
        for r in data["reviews"]:
            lst.append(fetchReview(r["_id"]))


class DSCJobsAPIResponse(object): 
    def __init__(self, **kwargs):
        
        for k in list(kwargs.keys()):
            self.__setattr__(k,kwargs.get(k))

def getendpoint(endpoint):
    r = requests.get(f"https://api.dscjobs.org/{endpoint}")
    r.raise_for_status()
    return DSCJobsAPIResponse(**r.json())

def fetchUser(userid,**context):
    """
    The fetchUser function retrieves a user's profile from the DSCJobs API.
    
    :param userid: Used to Pass the userid to fetchuser.
    :param **context: Used to Pass in any additional information that may be needed to process the request.
    :return: A .User() containing the user data.
    
    """
    
    with requests.get(f'https://api.dscjobs.org/user/{userid}') as resp:
        data = resp.json()
        resp.raise_for_status()
        if "error" in data:
            if resp.status == 400:
                raise MalformedRequest(userid,context)
            if resp.status == 404:
                raise UserNotFound(userid,context)
        data['created_at'] = data['duration']
        data['id'] = data['userID']
        resp.close()
        return User(data['id'],data['status']['banned'],data['status']['staff'],data['status']['premium'],data['premium']['lifetime'],data['premium']['duration'])

