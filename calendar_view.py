from model import Schedule
from schedule_view_model import CalenderViewModel, InvalidScheduleError, StringEntry
from datetime import date, datetime
from schedule_view import ScheduleDetailView
from TodoDetailView import TodoDetailView


class CalenderView:
    def __init__(self):
        self.viewmodel = CalenderViewModel()

    def load(self):
        while True:
            c = input("1: view calendar 2: create calendar 3: exit")
            if c == '1':
                try:
                    from_date = datetime.strptime(input("from time: "), "%Y-%m-%d %H:%M").date()
                    to_date = datetime.strptime(input("to time: "), "%Y-%m-%d %H:%M").date()
                    self.print_from_range(from_date, to_date)
                except ValueError:
                    print("Invalid input")
                    continue
            elif c == '2':
                self.create_schedule()
            elif c == '3':
                break
            else:
                continue


    def create_schedule(self):
        name = input("name: ")
        from_str = input("from time(YYYY-mm-dd HH:MM:SS): ")
        to_str = input("to time(YYYY-mm-dd HH:MM:SS): ")
        r = input("repeat? (yes:1 no:else): ")
        repeat = False
        if r == "1":
            repeat_day = input("repeat day(in binary, from sun~mon): ")
            interval = input("repeat interval(week): ")
            due = input("repeat due(YYYY-mm-dd): ")
            repeat = True
        else:
            repeat_day = ''
            interval = ''
            due = ''
        importance = input("importance: ")
        content = input("content: ")

        try:
            self.viewmodel.create_schedule(name=name, from_str=from_str, to_str=to_str, repeat=repeat, repeat_day=repeat_day, interval=interval, due=due,
                                           importance=importance, content=content)
            print("Successfully created: {0}".format(name))
        except InvalidScheduleError:
            print("Invalid argument. Please retry.")

    def print_from_range(self, from_date: date, to_date: date):
        entries = self.viewmodel.get_schedules(from_date, to_date)
        entries += self.viewmodel.get_todos(from_date, to_date)
        entries.sort(key=lambda x: x.date)
        for entry in entries:
            print(entry.string)

        while True:
            print('일정 상세보기: s{id}')
            print('TODO 상세보기: t{id}')
            print('종료: 엔터')
            s = input('>>> ')
            if not s:
                break
            t, id = s[0], int(s[1:])
            if t == 's':
                ScheduleDetailView(id).load()
            if t == 't':
                TodoDetailView(id).load()
            print()


if __name__ == '__main__':
    view = CalenderView()
    view.load()