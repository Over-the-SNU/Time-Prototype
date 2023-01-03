import schedule_view_model
from datetime import datetime, timedelta
from model import Schedule, Repeat
from constants import *

day_str = ['월', '화', '수', '목', '금', '토', '일']


class ScheduleDetailView:
    def __init__(self, id):
        self.id = id

    def load(self):
        print(f'일정 [{self.id}]')

        while True:
            self.retrieve()

            print('1. 편집')
            print('2. 삭제')
            print('3. 나가기')
            choice = int(input('>>> '))

            if choice == 1:
                self.update()
            if choice == 2:
                self.destroy()
            if choice == 3:
                break

    def retrieve(self):
        obj = schedule_view_model.get_detail(self.id)
        print(self.id, obj)
        if obj is None:
            print('해당 id를 가진 일정이 존재하지 않습니다.')
            return

        print(f'제목: {obj.name}')
        print(f'시작 시간: {obj.from_time}')
        print(f'종료 시간: {obj.to_time}')

        if obj.content:
            print(f'내용: {obj.content}')

        if obj.repeat:
            repeat_str = '반복: '
            if obj.repeat.due is not None:
                repeat_str += f'{obj.repeat.due}까지 '
            repeat_str += '매주 ' if obj.repeat.week_interval == 1 else f'{obj.repeat.week_interval}주 '
            repeat_str += ','.join(day for i, day in enumerate(day_str) if 1 << i & obj.repeat.day)
            print(repeat_str)

        if obj.importance:
            print(f'중요도: {obj.importance}')

    def update(self):
        print(f'수정할 항목을 선택하세요.')
        print('1. 제목')
        print('2. 시간')
        print('3. 내용')
        print('4. 반복')
        print('5. 중요도')
        choice = int(input('>>> '))

        if choice == 1:
            name = input('새 제목: ')
            schedule_view_model.update(self.id, name=name)

        if choice == 2:
            from_time = datetime.strptime(input('새 시작 시간 (yyyy-mm-dd HH:MM:SS): '), '%Y-%m-%d %H:%M:%S')
            to_time = datetime.strptime(input('새 종료 시간 (yyyy-mm-dd HH:MM:SS): '), '%Y-%m-%d %H:%M:%S')
            schedule_view_model.update(self.id, from_time=from_time, to=to_time)

        if choice == 3:
            content = input('새 내용: ')
            schedule_view_model.update(self.id, content=content)

        if choice == 4:
            print('새 반복')
            day = sum(1 << day_str.index(d) for d in input('요일 (콤마로 구분): ').split(','))
            week_interval = int(input('반복 간격 (주): '))
            due = datetime.strptime(input('만료 날짜 (yyyy-mm-dd): '), '%Y-%m-%d').date()
            schedule_view_model.update(self.id, repeat=Repeat(day=day, week_interval=week_interval, due=due))

        if choice == 5:
            importance = int(input('새 중요도: '))
            schedule_view_model.update(self.id, importance=importance)

    def destroy(self):
        code = schedule_view_model.delete(self.id)

        if code == CODE_ID_NOT_FOUND:
            print('해당 id를 가진 일정이 존재하지 않습니다.')
            return

        print('일정이 삭제되었습니다.')


assert schedule_view_model.create(from_time=datetime.now(),
                                  to_time=datetime.now() + timedelta(days=1),
                                  name='오더스 프로토타입 개발',
                                  content='캘린더 디테일 뷰 구현') == CODE_SUCCESS

print(Schedule.objects.all())

id = int(input('id: '))
ScheduleDetailView(id).load()
