from calendar_view import CalenderView
from todo_view import TodoListView


if __name__ == '__main__':
    print('1. 캘린더')
    print('2. TODO')
    choice = int(input('>>> '))

    if choice == 1:
        CalenderView().load()
    if choice == 2:
        TodoListView().load()
