import unittest
import models

from google.appengine.ext import ndb
from google.appengine.ext import testbed
from api.default.users import RegisterRequest
from api.default.users import RegisterResponse
from api.default.users import Users


class UsersApiTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_registration(self):
        # create the request
        request = RegisterRequest()
        request.name = 'Ismail Faizi'
        request.email = 'kanafghan@gmail.com'

        users_api = Users()
        response = users_api.register(request)

        self.assertTrue(None != response.user_key)

        user_key = ndb.Key(urlsafe=response.user_key)
        user = user_key.get()

        self.assertEqual(request.name, user.name)
        self.assertEqual(request.email, user.email)
