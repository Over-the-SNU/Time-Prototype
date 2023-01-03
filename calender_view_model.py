from model import *
import datetime
from model import CalenderEvent


class InvalidScheduleError(Exception):
    pass


class CalenderViewModel:
    def __init__(self):
        pass

    def create_schedule(self, **kwargs):
        if self.is_valid(**kwargs):
            raise InvalidScheduleError
        else:
            CalenderEvent.objects.create(CalenderEvent(**kwargs))

    def is_valid(self, **kwargs):
        try:
            if kwargs['name'] == '':
                return False
            from_time = datetime.datetime.strptime(kwargs['from_str'], "%Y-%m-%d %H:%M:%S")
            to_time = datetime.datetime.strptime(kwargs['to_str'], "%Y-%m-%d %H:%M:%S")
            if from_time > to_time:
                return False
            interval = int(kwargs['interval'])
            if interval < 0:
                return False
            due = datetime.datetime.strptime(kwargs['from_str'], "%Y-%m-%d").date()
            if due < to_time:
                return False
            importance = int(kwargs['importance'])
            if importance < 0:
                return False

        except:
            return False

    def get_schedules(self, from_date, to_date):
        pass

    def get_todos(self, from_date, to_date):
        pass
