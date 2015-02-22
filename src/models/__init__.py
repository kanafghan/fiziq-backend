'''
Created on 28/01/2015

@author: Ismail Faizi
'''
import os

from google.appengine.ext import ndb

APPLICATION_ID = os.environ['APPLICATION_ID']

USER_KEY = ndb.Key("User", 'root', app=APPLICATION_ID)
TRAINING_JOURNAL_KEY = ndb.Key("TrainingJournal", 'root', app=APPLICATION_ID)
WORKOUT_SESSION_KEY = ndb.Key("WorkoutSession", 'root', app=APPLICATION_ID)

class User(ndb.Model):
    """
    Representation of a user
    """
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)
    training_journal = ndb.KeyProperty(kind='TrainingJournal')


class TrainingJournal(ndb.Model):
    """
    Representation of a training journal
    """
    created_at = ndb.DateTimeProperty(auto_now_add=True)

    def get_user(self):
        return User.gql("WHERE training_journal = :1", self.key).get()


class WorkoutSession(ndb.Model):
    """
    Representation of a workout session
    """
    started_at = ndb.DateTimeProperty()
    ended_at = ndb.DateTimeProperty()
    training_journal = ndb.KeyProperty(kind='TrainingJournal')
    
