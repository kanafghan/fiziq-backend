'''
Created on 1/03/2015

@author: Ismail Faizi
'''
from common import AbstractPage
from models import MuscleGroup
from models.factories import ModelFactory
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import blobstore


class WorkoutsPage(blobstore_handlers.BlobstoreUploadHandler, AbstractPage):
    """
    Handler for workouts page
    """

    def __init__(self, request, response):
        super(WorkoutsPage, self).__init__('workouts.html', request, response)
        self.set_active_page('workouts')

    def add_common_values(self):
        self.add_template_value('form_url', blobstore.create_upload_url('/workouts'))
        self.add_template_value('muscle_groups', MuscleGroup.literals())

    def handle_get_request(self):
        self.add_common_values()

    def handle_post_request(self):
        self.add_common_values()

        muscle_group = self.request.get('muscle-group')
        if muscle_group == '0':
            self.add_message('You must select a Muscle Group!')
            return

        description = self.request.get('description', '')

        image1 = self.get_uploads('image1')
        if image1:
            image1 = image1[0].key()

        image2 = self.get_uploads('image2')
        if image2:
            image2 = image2[0].key()

        images = []
        if image1:
            images.append(image1)
        if image2:
            images.append(image2)

        names = self.request.get('names', '')
        names = names.split(';')

        workout = ModelFactory.create_workout(int(muscle_group), names, description, images)
        workout.put()

        self.add_message('Workout has been created successfully!', AbstractPage.MSG_TYPE_SUCCESS)
