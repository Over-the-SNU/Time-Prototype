from datetime import datetime
from todo_view_model import TodoViewModel
from model import Repeat

day_str = ['월', '화', '수', '목', '금', '토', '일']


class TodoListView:

    def __init__(self):
        self.viewmodel = TodoViewModel()

    def list(self):
        self.printlist()

    def search(self):
        print('검색할 항목을 선택하세요')
        print('1. 제목')
        print('2. 완료 여부')
        print('3. 진행도')
        print('4. 중요도')
        print('5. 내용')
        print('6. 날짜')
        choice = int(input('>>> '))

        if choice == 1:
            name = input('제목: ')
            self.printlist(name=name)

        if choice == 2:
            done = input('완료 여부(True/False): ')
            self.printlist(done=(done == 'True'))

        if choice == 3:
            progress = int(input('진행도: '))
            self.printlist(progress=progress)

        if choice == 4:
            importance = int(input('중요도: '))
            self.printlist(importance=importance)

        if choice == 5:
            content = input('내용: ')
            self.printlist(content=content)

        if choice == 6:
            date = datetime.strptime(input('날짜 (yyyy-mm-dd): '), '%Y-%m-%d').date()
            self.printlist(date=date)

    def printlist(self, **kwargs):
        for obj in self.viewmodel.get_list(**kwargs):
            print(f'제목: {obj.name}')
            print(f'완료 여부: {obj.done}')
            print(f'진행도: {obj.progress}')
            print(f'중요도: {obj.importance}')
            print(f'반복 날짜: {",".join(day for i, day in enumerate(day_str) if 1 << i & obj.repeat.day)}')
            print(f'반복 주기(주): {obj.repeat.week_interval}')
            print(f'만료 날짜: {obj.repeat.due.strftime("%Y-%m-%d")}')
            print(f'내용: {obj.content}')


    def create(self):
        date = datetime.strptime(input('날짜 (yyyy-mm-dd): '), '%Y-%m-%d').date()
        name = input('이름: ')
        content = input('내용: ')
        has_repeat = bool(input('반복 여부(True/False): '))
        repeat = None
        if has_repeat:
            day = sum(1 << day_str.index(d) for d in input('요일 (콤마로 구분): ').split(','))
            week_interval = int(input('반복 간격 (주): '))
            due = datetime.strptime(input('만료 날짜 (yyyy-mm-dd): '), '%Y-%m-%d').date()
            repeat = Repeat(day=day, week_interval=week_interval, due=due)
        progress = int(input('진행도: '))
        importance = int(input('중요도: '))

        self.viewmodel.create(date, name, content, repeat=repeat, done=False, progress=progress, importance=importance)

    def load(self):

        while True:
            print('1. 목록 출력')
            print('2. 검색')
            print('3. 추가')
            print('4. 종료')
            choice = int(input('>>> '))

            if choice == 1:
                self.list()
            if choice == 2:
                self.search()
            if choice == 3:
                self.create()
            if choice == 4:
                break


todo = TodoListView()
todo.load()
