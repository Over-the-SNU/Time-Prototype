import copy

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


@dataclass
class StringEntry:
    date: date
    string: str


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

    def get_schedules(self, from_date: date, to_date: date):
        schedules = Schedule.objects.all()
        ret = []
        for schedule in schedules:
            if from_date <= schedule.from_time.date() <= to_date:
                if schedule.repeat is None:
                    ret.append(StringEntry(schedule.from_time.date(), self.scheduleToStr(schedule)))
                else:
                    while schedule.from_time.date() <= to_date and schedule.from_time.date() <= schedule.repeat.due:
                        ret.append(StringEntry(schedule.from_time.date(), self.scheduleToStr(schedule)))
                        schedule.from_time = schedule.from_time + datetime.timedelta(days=7)
                        schedule.to_time = schedule.to_time + datetime.timedelta(days=7)
        return ret

    def get_todos(self, from_date: date, to_date: date):
        todos = Todo.objects.all()
        ret = []
        for todo in todos:
            if from_date <= todo.date <= to_date:
                if todo.repeat is None:
                    ret.append(StringEntry(todo.date, self.todoToStr(todo)))
                else:
                    while todo.date <= todo.repeat.due and todo.date <= to_date:
                        ret.append(StringEntry(todo.date, self.todoToStr(todo)))
                        todo.date = todo.date + datetime.timedelta(days=7)
        return ret

    def scheduleToStr(self, task):
        return "[Schedule] id={0}, name={1}, {2}~{3}".format(task.id, task.name,
                                                             task.from_time.strftime("%Y-%m-%d %H:%M:%S"),
                                                             task.to_time.strftime("%Y-%m-%d %H:%M:%S"))

    def todoToStr(self, task):
        return "[Todo] id={0} name={1}, {2}".format(task.id, task.name, task.date.strftime("%Y-%m-%d"))
