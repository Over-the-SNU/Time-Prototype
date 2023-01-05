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

        while self.retrieve():

            print('1. 편집')
            print('2. 삭제')
            print('3. 나가기')
            choice = int(input('>>> '))

            if choice == 1:
                self.update()
            if choice == 2:
                self.destroy()
                break
            if choice == 3:
                break

            print()

    def retrieve(self):
        obj = schedule_view_model.get_detail(self.id)
        if obj is None:
            print('존재하지 않는 일정입니다.')
            return False

        print(f'제목: {obj.name}')
        print(f'시작 시간: {obj.from_time.strftime("%Y-%m-%d %H:%M")}')
        print(f'종료 시간: {obj.to_time.strftime("%Y-%m-%d %H:%M")}')

        if obj.content:
            print(f'내용: {obj.content}')

        if obj.repeat:
            repeat_str = '반복: '
            if obj.repeat.due is not None:
                repeat_str += f'{obj.repeat.due}까지 '
            repeat_str += '매주 ' if obj.repeat.week_interval == 1 else f'{obj.repeat.week_interval}주 '
            repeat_str += ', '.join(day for i, day in enumerate(day_str) if 1 << i & obj.repeat.day)
            print(repeat_str)

        if obj.importance:
            print(f'중요도: {obj.importance}')

        return True

    def update(self):
        obj = schedule_view_model.get_detail(self.id)
        if obj is None:
            print('존재하지 않는 일정입니다.')
            return

        print(f'수정할 항목을 선택하세요.')
        print('1. 제목')
        print('2. 시간')
        print('3. 내용')
        print('4. 반복')
        print('5. 중요도')
        choice = int(input('>>> '))

        code = None

        if choice == 1:
            name = input('새 제목: ')
            code = schedule_view_model.update(self.id, name=name)

        if choice == 2:
            from_time = datetime.strptime(input('새 시작 시간 (yyyy-mm-dd HH:MM): '), '%Y-%m-%d %H:%M')
            to_time = datetime.strptime(input('새 종료 시간 (yyyy-mm-dd HH:MM): '), '%Y-%m-%d %H:%M')
            code = schedule_view_model.update(self.id, from_time=from_time, to_time=to_time)

        if choice == 3:
            content = input('새 내용: ')
            code = schedule_view_model.update(self.id, content=content)

        if choice == 4:
            remove_repeat = False
            if obj.repeat:
                print('기존 반복이 있습니다.')
                print('1. 반복 편집')
                print('2. 반복 제거')
                if int(input('>>> ')) == 2:
                    remove_repeat = True

            if remove_repeat:
                code = schedule_view_model.update(self.id, repeat=None)
            else:
                print('새 반복')
                day = sum(1 << day_str.index(d) for d in input('요일 (콤마로 구분): ').split(','))
                week_interval = int(input('반복 간격 (주): '))
                due = datetime.strptime(input('만료 날짜 (yyyy-mm-dd): '), '%Y-%m-%d').date()
                code = schedule_view_model.update(self.id, repeat=Repeat(day=day, week_interval=week_interval, due=due))

        if choice == 5:
            remove_importance = False
            if obj.importance:
                print('기존 중요도가 있습니다.')
                print('1. 중요도 편집')
                print('2. 중요도 제거')
                if int(input('>>> ')) == 2:
                    remove_importance = True

            if remove_importance:
                code = schedule_view_model.update(self.id, importance=0)
            else:
                importance = int(input('새 중요도: '))
                code = schedule_view_model.update(self.id, importance=importance)

        if code == CODE_SUCCESS:
            print('일정이 수정되었습니다.')
        elif code == CODE_INVALID_DATE:
            print('유효하지 않은 시작 시간과 종료 시간입니다.')
        elif code == CODE_TITLE_EMPTY:
            print('제목이 비어 있습니다.')
        elif code == CODE_ID_NOT_FOUND:
            print('존재하지 않는 일정입니다.')
        else:
            print(f'내부 오류로 실패하였습니다. ({code})')

    def destroy(self):
        code = schedule_view_model.delete(self.id)

        if code == CODE_ID_NOT_FOUND:
            print('존재하지 않는 일정입니다.')
            return

        print('일정이 삭제되었습니다.')


if __name__ == '__main__':
    # schedule_view_model.create(from_time=datetime.now(),
    #                                   to_time=datetime.now() + timedelta(days=1),
    #                                   name='오더스 프로토타입 개발',
    #                                   content='캘린더 디테일 뷰 구현')

    print(Schedule.objects.all())

    id = int(input('id: '))
    ScheduleDetailView(id).load()
