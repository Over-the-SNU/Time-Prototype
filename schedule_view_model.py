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
    id = 0  # TODO: should ViewModel assign id?

    try:
        obj = Schedule(id=id, **kwargs)
    except TypeError:
        return CODE_INVALID_ARGUMENTS  # mismatched types or missing required field

    code = validate(obj)

    if code == CODE_SUCCESS:
        Schedule.objects.create(obj)

    return code


def get_detail(id: int):
    obj = Schedule.objects.get(id)
    # TODO: handle when id does not exist
    return obj


def update(id: int, **kwargs):
    obj = Schedule.objects.get(id)
    # TODO: handle when id does not exist

    for attr, value in kwargs.items():
        setattr(obj, attr, value)

    code = validate(obj)

    if code == CODE_SUCCESS:
        Schedule.objects.update(id, obj)

    return code


def delete(id: int, **kwargs):
    obj = Schedule.objects.delete(id)
    # TODO: handle when id does not exist
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
