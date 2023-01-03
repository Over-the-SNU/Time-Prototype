from datetime import date

class TodoViewModel:
    def __init__(self, name, importance, done, progress, dueDate, repeat, content):
        self.name = name
        self.importance = importance
        self.done = done
        self.progress = progress
        self.date = dueDate
        self.repeat = repeat
        self.content = content
    def modify(self, place, content):
        if place == 1:
            if isinstance(content, str):
                self.name = content
                return True
            else:
                return False
        elif place == 2:
            try:
                self.importance = int(content)
                return True
            except ValueError:
                return False
        elif place == 3:
            self.done = not self.done
        elif place == 4:
            try:
                self.progress = int(content)
                return True
            except ValueError:
                return False
        elif place == 5:
            try:
                self.date = date(content)
                return True
            except ValueError:
                return False
        elif place == 6:
            if isinstance(content, str):
                self.repeat = content
                return True
            else:
                return False
        elif place == 7:
            self.content = content
            return True
        else:
            return False
    def __del__(self):
        pass