from datetime import date
from model import Todo

class TodoViewModel:
    def __init__(self):# name, importance, done, progress, dueDate, repeat, content):
        pass
        # self.name = name
        # self.importance = importance
        # self.done = done
        # self.progress = progress
        # self.date = dueDate
        # self.repeat = repeat
        # self.content = content
    def get(self, id):
        Todo.objects.get(id)
    def update(self, id, place, content):
        obj = Todo.objects.get(id)
        if place == 1:
            if isinstance(content, str):
                obj.name = content
                Todo.objects.update(id, obj)
                return True
            else:
                return False
        elif place == 2:
            try:
                obj.importance = int(content)
                Todo.objects.update(id, obj)
                return True
            except ValueError:
                return False
        elif place == 3:
            obj.done = not obj.done
            Todo.objects.update(id, obj)
        elif place == 4:
            try:
                obj.progress = int(content)
                Todo.objects.update(id, obj)
                return True
            except ValueError:
                return False
        elif place == 5:
            try:
                obj.date = date(content)
                Todo.objects.update(id, obj)
                return True
            except ValueError:
                return False
        elif place == 6:
            if isinstance(content, str):
                obj.repeat = content
                Todo.objects.update(id, obj)
                return True
            else:
                return False
        elif place == 7:
            obj.content = content
            Todo.objects.update(id, obj)
            return True
        else:
            return False
    def __del__(self, id):
        Todo.objects.delete(id)