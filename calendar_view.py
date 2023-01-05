from model import Schedule
from schedule_view_model import CalenderViewModel, InvalidScheduleError, StringEntry
from datetime import date, datetime


class CalenderView:
    def __init__(self):
        self.viewmodel = CalenderViewModel()

    def load(self):
        while True:
            c = input("1: view calendar 2: exit")
            if c == '1':
                try:
                    from_date = datetime.strptime(input("from time: "), "%Y-%m-%d %H:%M:%S").date()
                    to_date = datetime.strptime(input("to time: "), "%Y-%m-%d %H:%M:%S").date()
                    self.print_from_range(from_date, to_date)
                except:
                    print("Invalid input")
                    continue
            else:
                break


    def create_schedule(self):
        name = input("name: ")
        from_str = datetime.strptime(input("from time: "), "%Y-%m-%d %H:%M:%S")
        to_str = datetime.strptime(input("to time: "), "%Y-%m-%d %H:%M:%S")
        interval = input("repeat interval: ")
        due = input("repeat due: ")
        importance = input("importance: ")
        content = input("content: ")

        try:
            self.viewmodel.create_schedule(name=name, from_str=from_str, to_str=to_str, interval=interval, due=due,
                                           importance=importance, content=content)
            print("Successfully created: {0}".format(name))
        except InvalidScheduleError:
            print("Invalid argument. Please retry.")

    def print_from_range(self, from_date: date, to_date: date):
        entries = self.viewmodel.get_schedules(from_date, to_date)
        entries += self.viewmodel.get_todos(from_date, to_date)
        entries.sort(key=lambda x: x.date)
        for entry in entries:
            print(entry)


