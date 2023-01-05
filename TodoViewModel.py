import datetime
from datetime import datetime
from model import Todo, Repeat


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
        return Todo.objects.get(id)

    def update(self, id, place, content):
        obj = Todo.objects.get(id)
        if place == 1:
            if isinstance(content, str):
                if content != "":
                    obj.name = content
                    Todo.objects.update(id, obj)
                    return True
                else:
                    return False
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
            return True
        elif place == 4:
            try:
                obj.progress = int(content)
                Todo.objects.update(id, obj)
                return True
            except ValueError:
                return False
        elif place == 5:
            try:
                obj.date = datetime.strptime(content, "%Y-%m-%d").date()
                Todo.objects.update(id, obj)
                return True
            except ValueError:
                return False
        elif place == 6:
            try:
                day = int(content[0])
                week_interval = int(content[1])
                if week_interval <= 0:
                    return False
                due = datetime.strptime(content[2], "%Y-%m-%d").date()
                if due < obj.date:
                    return False
                obj.repeat = Repeat(day, week_interval, due)
                Todo.objects.update(id, obj)
                return True
            except ValueError:
                return False
        elif place == 7:
            obj.content = content
            Todo.objects.update(id, obj)
            return True
        else:
            return False

    def delete(self, id):
        Todo.objects.delete(id)
