from model import Todo
from constants import *
import datetime


class TodoViewModel():

    def __init__(self):
        pass

    def validate(self, obj):

        if obj.name == '':
            return CODE_TITLE_EMPTY

        if obj.progress < 0:
            return CODE_INVALID_PROGRESS

        if obj.importance < 0:
            return CODE_INVALID_IMPORTANCE

        if obj.repeat is not None and obj.repeat.due < obj.date:
            return CODE_INVALID_DATE

        return CODE_SUCCESS

    def create(self, date, name, content, **kwargs):

        id = 0
        # Todo: id 변경
        repeat = kwargs.get("repeat")
        done = kwargs.get("done")
        progress = kwargs.get("progress")
        importance = kwargs.get("importance")

        obj = Todo(id=id, name=name, date=date, content=content, repeat=repeat, done=done, progress=progress,
                   importance=importance)

        if self.validate(obj) == CODE_SUCCESS:
            Todo.objects.create(obj)
        else:
            return self.validate(obj)

    def get_list(self, **kwargs):

        l = []
        for obj in Todo.objects.all():
            if all(getattr(obj, attr) == value for attr, value in kwargs.items()):
                l.append(obj)
        return l