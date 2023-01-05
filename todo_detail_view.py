from todo_detail_view_model import TodoViewModel


class TodoDetailView:
    def __init__(self, id):
        self.id = id
        self.viewModel = TodoViewModel()

    def load(self):
        reload = True
        while reload:
            obj = self.viewModel.get(self.id)
            print(f"Todo: {obj.name} (중요도: {obj.importance})")
            if obj.done:
                print("완료됨")
            else:
                print(f"진행도: {obj.progress}")

            print(f"시간: {obj.date}")
            print(f"반복: {obj.repeat}")
            print(f"메모: {obj.content}")
            print("--------")
            print("1. 편집")
            print("2. 삭제")
            print("3. 나가기")

            action_select_is_ok = False
            while not action_select_is_ok:
                button = input()
                if button == "1":
                    edit_is_ok = False
                    while not edit_is_ok:
                        print(f"1. Todo: {obj.name}")
                        print(f"2. 중요도: {obj.importance}")
                        print(f"3. 완료: {obj.done}")
                        print(f"4. 진행도: {obj.progress}")
                        print(f"5. 시간: {obj.date}")
                        print(f"6. 반복: {obj.repeat}")
                        print(f"7. 메모: {obj.content}")
                        try:
                            place = int(input("편집할 위치를 정하세요(취소: 0):"))
                        except ValueError:
                            place_is_ok = False
                            while not place_is_ok:
                                try:
                                    place = int(input("편집할 위치를 다시 입력하세요(취소: 0):"))
                                    place_is_ok = True
                                except ValueError:
                                    pass

                        if place == 0:
                            print("취소되었습니다.")
                            edit_is_ok = True
                            action_select_is_ok = True
                        elif place == 3:
                            edit_is_ok = self.viewModel.update(self.id, place, "")
                            print("변경되었습니다")
                            action_select_is_ok = True
                        elif place == 6:
                            day = input("반복할 요일을 입력하세요:")
                            week_interval = input("몇 주를 주기로 반복할 지 입력하세요:")
                            due = input("반복을 마칠 날짜를 입력하세요:")
                            edit_is_ok = self.viewModel.update(self.id, place, [day, week_interval, due])
                            if edit_is_ok:
                                print("완료됐습니다")
                                action_select_is_ok = True
                            else:
                                print("다시 입력해주세요")
                        elif 0 < place <= 7:
                            content = input("내용을 입력하세요:")
                            edit_is_ok = self.viewModel.update(self.id, place, content)
                            if edit_is_ok:
                                print("완료됐습니다")
                                action_select_is_ok = True
                            else:
                                print("다시 입력해주세요")
                        else:
                            print("다시 입력해주세요")
                elif button == "2":
                    self.viewModel.delete(self.id)
                    action_select_is_ok = True
                    reload = False
                elif button == "3":
                    action_select_is_ok = True
                    reload = False
                else:
                    print("다시 입력해주세요")
