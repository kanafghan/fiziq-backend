import unittest

import models

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from api.default.workouts import SetMessage
from api.default.workouts import SessionCreateRequest
from api.default.workouts import WorkoutMessage
from api.default.workouts import Workouts
from models.factories import ModelFactory


class WorkoutsApiTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        self.training_journals = [
            ModelFactory.create_training_journal()
        ]
        for journal in self.training_journals:
            journal.put()

        self.users = [
            ModelFactory.create_user(name='Iceman', email='is@mail.com', training_journal=self.training_journals[0])
        ]
        for user in self.users:
            user.put()

    def tearDown(self):
        self.testbed.deactivate()

    def test_create_workout_session_when_workouts_dont_exist(self):
        # create the request
        set_msg = SetMessage()
        set_msg.weight = 10.0
        set_msg.reps = 10

        workout_msg = WorkoutMessage()
        workout_msg.name = 'Front Raises'
        workout_msg.sets = [set_msg]

        request = SessionCreateRequest()
        request.started_at = '2016-04-04T18:43:24.244Z'
        request.ended_at = '2016-04-04T19:16:00.659Z'
        request.workouts = [workout_msg]
        request.user_key = self.users[0].key.urlsafe()

        workouts_api = Workouts()
        response = workouts_api.create_workout_session(request)

        self.assertIsNot(response.session_key, None)

        # TODO do assertion about workouts and sets has been created
