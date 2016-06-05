'''
Created on 08/03/2015

@author: Ismail Faizi
'''
import endpoints

from protorpc import messages
from protorpc import remote
from protorpc import message_types
from api.default import defaultApi
from api.default import Utilities
from models import User
from models import Workout
from models import MuscleGroup
from models.factories import ModelFactory


'''
### MESSAGES ###
'''
class ListResponse(messages.Message):
    pass


class SetMessage(messages.Message):
    weight = messages.FloatField(1, required=True)
    reps = messages.IntegerField(2, required=True)


class WorkoutMessage(messages.Message):
    workout_key = messages.StringField(1)
    name = messages.StringField(2)
    duration = messages.IntegerField(3)
    sets = messages.MessageField(SetMessage, 4, repeated=True)


class SessionCreateRequest(messages.Message):
    user_key = messages.StringField(1, required=True)
    started_at = messages.StringField(2, required=True)
    ended_at = messages.StringField(3, required=True)
    workouts = messages.MessageField(WorkoutMessage, 4, repeated=True)


class SessionCreateResponse(messages.Message):
    session_key = messages.StringField(1, required=True)


class SetCreateRequest(messages.Message):
    pass


class SetCreateResponse(messages.Message):
    pass

'''
### END of MESSAGES ###
'''


@defaultApi.api_class(
    resource_name='workouts',
    path='workouts'
)
class Workouts(remote.Service):
    """
    API for workouts, workout sessions and workout sets
    """

    @endpoints.method(
        message_types.VoidMessage,
        ListResponse,
        name='list',
        path='list',
        http_method='GET'
    )
    def list(self, request):
        """
        Returns a list of workouts
        """
        pass

    @endpoints.method(
        SessionCreateRequest,
        SessionCreateResponse,
        name='sessions.create',
        path='sessions/create',
        http_method='POST'
    )
    def create_workout_session(self, request):
        """
        Creates a workout session based on the given data
        """
        user = Utilities.load_entity(User, request.user_key)

        training_journal = user.training_journal.get() if user.training_journal else None
        if not training_journal:
            training_journal = ModelFactory.create_training_journal()
            training_journal.put()
            user.training_journal = training_journal.key

        start_time = Utilities.parse_date(request.started_at)
        if not start_time:
            raise endpoints.BadRequestException('Start time is not provided!')

        end_time = Utilities.parse_date(request.ended_at)
        if not end_time:
            raise endpoints.BadRequestException('End time is not provided!')

        session = ModelFactory.create_workout_session(start_time, end_time, training_journal)
        session.put()

        # TODO duration = messages.IntegerField(3)

        for workout_msg in request.workouts:
            workout = None
            if workout_msg.workout_key:
                workout = Utilities.load_entity(Workout, workout_msg.workout_key)

            # TODO search for the workout by name

            if not workout:
                workout = ModelFactory.create_workout(MuscleGroup.CHEST, [workout_msg.name])
                workout.put()

            for set_msg in workout_msg.sets:
                workout_set = ModelFactory.create_workout_set(repetitions=set_msg.reps,
                                                              weight=set_msg.weight,
                                                              workout_session=session,
                                                              workout=workout)
                workout_set.put()

        return SessionCreateResponse(session_key=session.key.urlsafe())

    @endpoints.method(
        SetCreateRequest,
        SetCreateResponse,
        name='set.create',
        path='set/create',
        http_method='POST'
    )
    def create_workout_set(self, request):
        """
        Creates a workout set based on the given data
        """
        pass
