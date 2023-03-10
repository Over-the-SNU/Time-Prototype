from datetime import datetime

from todo_detail_view import TodoDetailView
from constants import *
from model import Repeat
from todo_view_model import TodoViewModel

DAY_STR = ('월', '화', '수', '목', '금', '토', '일')


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
            try:
                progress = int(input('진행도: '))
                self.printlist(progress=progress)
            except ValueError:
                print("정수를 입력하세요.")

        if choice == 4:
            try:
                importance = int(input('중요도: '))
                self.printlist(importance=importance)
            except ValueError:
                print("정수를 입력하세요.")

        if choice == 5:
            content = input('내용: ')
            self.printlist(content=content)

        if choice == 6:
            try:
                date = datetime.strptime(input('날짜 (yyyy-mm-dd): '), '%Y-%m-%d').date()
                self.printlist(date=date)
            except ValueError:
                print('잘못된 형식입니다.')

    def printlist(self, **kwargs):
        for obj in self.viewmodel.get_list(**kwargs):
            print(f'날짜: {obj.date.strftime("%Y-%m-%d")}')
            print(f'제목: {obj.name}')
            print(f'완료 여부: {obj.done}')
            print(f'진행도: {obj.progress}')
            print(f'중요도: {obj.importance}')
            if obj.repeat:
                print(f'반복 날짜: {",".join(day for i, day in enumerate(DAY_STR) if 1 << i & obj.repeat.day)}')
                print(f'반복 주기(주): {obj.repeat.week_interval}')
                print(f'만료 날짜: {obj.repeat.due.strftime("%Y-%m-%d")}')
            print(f'내용: {obj.content}')
            print()

        while True:
            print('TODO 상세보기: {id}')
            print('종료: 엔터')
            s = input('>>> ')
            if not s:
                break
            id = int(s)
            TodoDetailView(id).load()
            print()

    def create(self):
        try:
            date = datetime.strptime(input('날짜 (yyyy-mm-dd): '), '%Y-%m-%d').date()
        except ValueError:
            print('잘못된 형식입니다.')
            return
        name = input('이름: ')
        content = input('내용: ')
        has_repeat = input('반복 여부(True/False): ')
        repeat = None
        if has_repeat == 'True':
            try:
                day = sum(1 << DAY_STR.index(d) for d in input('요일 (콤마로 구분): ').split(','))
            except ValueError:
                print('잘못된 형식입니다.')
                return
            try:
                week_interval = int(input('반복 간격 (주): '))
            except ValueError:
                print("정수를 입력하세요.")
                return
            try:
                due = datetime.strptime(input('만료 날짜 (yyyy-mm-dd): '), '%Y-%m-%d').date()
            except ValueError:
                print('잘못된 형식입니다.')
                return
            repeat = Repeat(day=day, week_interval=week_interval, due=due)

        try:
            progress = int(input('진행도: '))
        except ValueError:
            print("정수를 입력하세요.")
            return
        try:
            importance = int(input('중요도: '))
        except ValueError:
            print("정수를 입력하세요.")
            return
        v = self.viewmodel.create(date, name, content, repeat=repeat,
                                  done=False, progress=progress, importance=importance)
        if v == CODE_INVALID_DATE:
            print('날짜가 잘못되었습니다.')
        elif v == CODE_INVALID_PROGRESS:
            print('진행도가 잘못되었습니다.')
        elif v == CODE_INVALID_IMPORTANCE:
            print('중요도가 잘못되었습니다.')

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


if __name__ == '__main__':
    todo = TodoListView()
    todo.load()
