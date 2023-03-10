import copy
import dataclasses
import datetime

from constants import *
from model import *
from model import Schedule


def validate(**kwargs):
    kwargs['id'] = 0
    try:
        obj = Schedule(**kwargs)
    except (ValueError, TypeError):
        return CODE_INVALID_ARGUMENTS

    if obj.from_time > obj.to_time or (obj.repeat and obj.to_time > obj.repeat.due):
        return CODE_INVALID_DATE

    if not obj.name:
        return CODE_TITLE_EMPTY

    if obj.repeat is not None:  # TODO: validation for repeat
        pass

    if obj.importance is not None:  # TODO: validation for importance
        pass

    return CODE_SUCCESS


def create(**kwargs):
    code = validate(**kwargs)

    if code == CODE_SUCCESS:
        Schedule.objects.create(**kwargs)

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

    code = validate(**(dataclasses.asdict(obj) | kwargs))

    if code == CODE_SUCCESS:
        Schedule.objects.update(id, **kwargs)

    return code


def delete(id: int):
    try:
        Schedule.objects.delete(id)
    except ValueError:
        return CODE_ID_NOT_FOUND
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
            from_time = datetime.datetime.strptime(kwargs['from_str'], "%Y-%m-%d %H:%M:%S")
            to_time = datetime.datetime.strptime(kwargs['to_str'], "%Y-%m-%d %H:%M:%S")
            if kwargs['repeat']:
                repeat = Repeat(int(kwargs['repeat_day'], 2), int(kwargs['interval']), datetime.datetime.strptime(kwargs['due'], "%Y-%m-%d").date())
            else:
                repeat = None
            Schedule.objects.create(Schedule(id=0, name=kwargs['name'],from_time=from_time, to_time=to_time, repeat=repeat,
                                             importance=kwargs['importance'], content=kwargs['content']))
        else:
            raise InvalidScheduleError

    @staticmethod
    def is_valid(**kwargs):
        try:
            if kwargs['name'] == '':
                return False
            from_time = datetime.datetime.strptime(kwargs['from_str'], "%Y-%m-%d %H:%M:%S")
            to_time = datetime.datetime.strptime(kwargs['to_str'], "%Y-%m-%d %H:%M:%S")
            if from_time > to_time:
                return False
            if kwargs['repeat']:
                repeat_day = int(kwargs['repeat_day'], 2)
                if repeat_day < 0b0000001 or repeat_day > 0b1000000:
                    return False
                interval = int(kwargs['interval'])
                if interval <= 0:
                    return False
                due = datetime.datetime.strptime(kwargs['due'], "%Y-%m-%d").date()
                if due < to_time.date():
                    return False
            importance = int(kwargs['importance'])
            if importance < 0:
                return False
            return True
        except ValueError:
            return False

    def get_schedules(self, from_date: date, to_date: date):
        schedules = Schedule.objects.all()
        ret = []
        for schedule in schedules:
            if from_date <= schedule.from_time.date() <= to_date:
                if schedule.repeat is None:
                    ret.append(StringEntry(schedule.from_time.date(), self.schedule_to_str(schedule)))
                else:
                    ret.append(StringEntry(schedule.from_time.date(), self.schedule_to_str(schedule)))

                    diff = 0 - schedule.from_time.weekday()
                    ls = []
                    b = 0b0000001
                    while b <= 0b1000000:
                        if schedule.repeat.day & b != 0:
                            s = copy.deepcopy(schedule)
                            s.from_time = s.from_time + datetime.timedelta(days=diff)
                            s.to_time = s.to_time + datetime.timedelta(days=diff)
                            ls.append(s)
                        b = b << 1
                        diff += 1
                    for sc in ls:
                        while sc.from_time.date() <= schedule.repeat.due and sc.from_time.date() <= to_date:
                            if sc.from_time.date() >= from_date and sc.from_time.date() >= schedule.from_time.date():
                                ret.append(StringEntry(sc.from_time.date(), self.schedule_to_str(sc)))
                            sc.from_time = sc.from_time + datetime.timedelta(days=7*schedule.repeat.week_interval)
                            sc.to_time = sc.to_time + datetime.timedelta(days=7*schedule.repeat.week_interval)

        return ret

    def get_todos(self, from_date: date, to_date: date):
        todos = Todo.objects.all()
        ret = []
        for todo in todos:
            if from_date <= todo.date <= to_date:
                if todo.repeat is None:
                    ret.append(StringEntry(todo.date, self.todo_to_str(todo)))
                else:
                    while todo.date <= todo.repeat.due and todo.date <= to_date:
                        ret.append(StringEntry(todo.date, self.todo_to_str(todo)))
                        todo.date = todo.date + datetime.timedelta(days=7)
        return ret

    @staticmethod
    def schedule_to_str(task):
        return "[Schedule] id={0}, name={1}, {2}~{3}".format(task.id, task.name,
                                                             task.from_time.strftime("%Y-%m-%d %H:%M:%S"),
                                                             task.to_time.strftime("%Y-%m-%d %H:%M:%S"))

    @staticmethod
    def todo_to_str(task):
        return "[Todo] id={0} name={1}, {2}".format(task.id, task.name, task.date.strftime("%Y-%m-%d"))
