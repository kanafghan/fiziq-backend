'''
Created on 08/03/2015

@author: Ismail Faizi
'''
import datetime
import endpoints
import re

defaultApi = endpoints.api(
    name='default',
    version='v1',
    title='Fiziq Default API',
    description='The API for Fiziq smarthphone applications.'
)

class Utilities(object):
    """
    Utility logic for default API endpoints
    """

    @classmethod
    def load_entity(cls, class_name, key):
        entity = class_name.get_by_urlsafe_key(key)
        if not entity:
            message = 'No {} with the key "{}" exists!'.format(class_name.__name__, key)
            raise endpoints.NotFoundException(message)

        return entity

    @classmethod
    def validate_email(cls, email):
        m = re.match(r'^\S+@\S+\.\S+$', email)
        if not m:
            message = '{} is not a valid E-mail address!'.format(email)
            raise endpoints.BadRequestException(message)

        return email

    @classmethod
    def parse_date(cls, date, default=None, format="%Y-%m-%dT%H:%M:%S.%fZ"):
        try:
            date = datetime.datetime.strptime(date, format)

            return date
        except ValueError, ve:
            pass

        return default
