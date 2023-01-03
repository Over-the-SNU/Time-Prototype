from calender_view_model import CalenderViewModel, InvalidScheduleError
import datetime

class CalenderView:
    def __init__(self):
        self.viewmodel = CalenderViewModel

    def create_schedule(self):
        name = input("name: ")
        from_str = datetime.datetime.strptime(input("from time: "), "%Y-%m-%d %H:%M:%S")
        to_str = datetime.datetime.strptime(input("from time: "), "%Y-%m-%d %H:%M:%S")
        interval = input("repeat interval: ")
        due = input("repeat due: ")
        importance = input("importance: ")
        content = input("content: ")

        try:
            self.viewmodel.create_schedule(name=name, from_str=from_str, to_str=to_str, interval=interval, due=due, importance=importance, content=content)
            print("Successfully created: {0}".format(name))
        except InvalidScheduleError:
            print("Invalid argument. Please retry.")

    def print_from_range(self, from_date, to_date):
        pass