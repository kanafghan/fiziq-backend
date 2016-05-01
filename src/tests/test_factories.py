import unittest
import datetime
import models

from google.appengine.ext import testbed
from google.appengine.ext.ndb.blobstore import BlobKey
from models.factories import ModelFactory


class ModelFactoryTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_create_training_journal(self):
        # create a journal
        journal = ModelFactory.create_training_journal()
        self.assertTrue(isinstance(journal, models.TrainingJournal))

    def test_create_user(self):
        # create a user
        journal = ModelFactory.create_training_journal()
        journal.put()

        user = ModelFactory.create_user('Iceman', 'if@kanafghan.com', journal)

        # the user should be as expected
        self.assertTrue(isinstance(user, models.User))
        self.assertEqual(user.name, 'Iceman')
        self.assertEqual(user.email, 'if@kanafghan.com')
        self.assertEqual(user.training_journal, journal.key)

    def test_create_workout_session(self):
        # create a workout session
        journal = ModelFactory.create_training_journal()
        journal.put()

        started_at = datetime.datetime.now()
        ended_at = started_at + datetime.timedelta(hours=+1)
        ws = ModelFactory.create_workout_session(started_at, ended_at, journal)

        # the workout session should be as expected
        self.assertTrue(isinstance(ws, models.WorkoutSession))
        self.assertEqual(ws.started_at, started_at)
        self.assertEqual(ws.ended_at, ended_at)
        self.assertEqual(ws.training_journal, journal.key)

    def test_create_workout(self):
        muscle = models.MuscleGroup.CHEST
        names = ['Bench Press', 'Barbell Bench Press']
        desc = 'description of how the workout is performed'
        images = [BlobKey('img1'), BlobKey('img2')]
        workout = ModelFactory.create_workout(muscle, names, desc, images)

        # the workout should be as expected
        self.assertTrue(isinstance(workout, models.Workout))
        self.assertEqual(workout.muscle_group, muscle)
        self.assertEqual(workout.names, names)
        self.assertEqual(workout.description, desc)
        self.assertEqual(workout.images, images)

    def test_create_workout_set(self):
        # create a workout set
        journal = ModelFactory.create_training_journal()
        journal.put()

        started_at = datetime.datetime.now()
        ended_at = started_at + datetime.timedelta(hours=+1)
        ws = ModelFactory.create_workout_session(started_at, ended_at, journal)
        ws.put()

        workout = ModelFactory.create_workout(models.MuscleGroup.CHEST, ['Bench Press'])
        workout.put()

        workout_set = ModelFactory.create_workout_set(10, 50, ws, workout)

        # the workout session should be as expected
        self.assertTrue(isinstance(workout_set, models.WorkoutSet))
        self.assertEqual(workout_set.repetitions, 10)
        self.assertEqual(workout_set.weight, 50)
        self.assertEqual(workout_set.workout_session, ws.key)
        self.assertEqual(workout_set.workout, workout.key)
