from constants import *
from model import *
import datetime
from model import Schedule


def validate(obj: Schedule):
    if obj.from_time > obj.to_time:
        return CODE_INVALID_DATE

    if not obj.name:
        return CODE_TITLE_EMPTY

    if obj.repeat is not None:  # TODO: validation for repeat
        pass

    if obj.importance is not None:  # TODO: validation for importance
        pass

    return CODE_SUCCESS


def create(**kwargs):
    id = 0  # TODO

    try:
        obj = Schedule(id=id, **kwargs)
    except TypeError:
        return CODE_INVALID_ARGUMENTS  # mismatched types or missing required field

    code = validate(obj)

    if code == CODE_SUCCESS:
        Schedule.objects.create(obj)

    return code


def get_detail(id: int):
    try:
        obj = Schedule.objects.get(id)
    except ValueError:
        return None
    return obj


def update(id: int, **kwargs):
    try:
        obj = Schedule.objects.get(id)
    except ValueError:
        return CODE_ID_NOT_FOUND

    for attr, value in kwargs.items():
        setattr(obj, attr, value)

    code = validate(obj)

    if code == CODE_SUCCESS:
        Schedule.objects.update(id, obj)

    return code


def delete(id: int):
    try:
        Schedule.objects.get(id)
    except ValueError:
        return CODE_ID_NOT_FOUND

    Schedule.objects.delete(id)

    return CODE_SUCCESS


class InvalidScheduleError(Exception):
    pass


class CalenderViewModel:
    def __init__(self):
        pass

    def create_schedule(self, **kwargs):
        if self.is_valid(**kwargs):
            raise InvalidScheduleError
        else:
            Schedule.objects.create(Schedule(**kwargs))

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
