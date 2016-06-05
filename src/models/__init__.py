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
WORKOUT_SET_KEY = ndb.Key("WorkoutSet", 'root', app=APPLICATION_ID)
WORKOUT_KEY = ndb.Key("Workout", 'root', app=APPLICATION_ID)


class AbstractModel(ndb.Model):

    @classmethod
    def get_by_urlsafe_key(cls, urlsafe_key):
        try:
            key = ndb.Key(urlsafe=urlsafe_key)

            return key.get()
        except:
            pass  # Just ignore it

        return None


class MuscleGroup(object):
    """
    Enumeration that enumerates the 7 major muscle groups
    """
    CHEST = 1
    SHOULDERS = 2
    BACK = 3
    BICEPS = 4
    TRICEPS = 5
    LEGS = 6
    ABS = 7


    @classmethod
    def values(cls):
        return [1, 2, 3, 4, 5, 6, 7]


    @classmethod
    def literals(cls):
        return ['CHEST', 'SHOULDERS', 'BACK', 'BICEPS', 'TRICEPS', 'LEGS', 'ABS']


class User(AbstractModel):
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


class WorkoutSet(ndb.Model):
    """
    Representation of a workout set, i.e. repetitions
    of a specific workout with a specific weight
    """
    repetitions = ndb.IntegerProperty()
    weight = ndb.FloatProperty()
    workout_session = ndb.KeyProperty(kind='WorkoutSession')
    workout = ndb.KeyProperty(kind='Workout')


class Workout(ndb.Model):
    """
    Representation of a physical exercise targetting one or
    more muscle groups
    """
    names = ndb.StringProperty(repeated=True)
    muscle_group = ndb.IntegerProperty(choices=MuscleGroup.values(), required=True)
    description = ndb.StringProperty()
    images = ndb.BlobKeyProperty(repeated=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
