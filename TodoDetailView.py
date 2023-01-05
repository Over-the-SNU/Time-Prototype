from TodoViewModel import TodoViewModel
class TodoDetailView:
    def __init__(self, id):
        self.id = id
    def loadView(self):
        reload = True
        while reload:
            viewModel = TodoViewModel().get(id)
            print(f"Todo: {viewModel.name} (중요도: {viewModel.importance})")
            if self.viewModel.done:
                print("완료됨")
            else:
                print(f"진행도: {viewModel.progress}")

            print(f"시간: {viewModel.date}")
            print(f"반복: {viewModel.repeat}")
            print(f"메모: {viewModel.content}")
            print("--------")
            print("1. 편집")
            print("2. 삭제")
            print("3. 나가기")

            actionSelectIsOK = False
            while not actionSelectIsOK:
                button = input()
                if button == "1":
                    editIsOK = False
                    while not editIsOK:
                        print(f"1. Todo: {viewModel.name}")
                        print(f"2. 중요도: {viewModel.importance}")
                        print(f"3. 완료: {viewModel.done}")
                        print(f"4. 진행도: {viewModel.progress}")
                        print(f"5. 시간: {viewModel.date}")
                        print(f"6. 반복: {viewModel.repeat}")
                        print(f"7. 메모: {viewModel.content}")
                        try:
                            place = int(input("편집할 위치를 정하세요(취소: 0):"))
                        except ValueError:
                            placeIsOK = False
                            while not placeIsOK:
                                try:
                                    place = int(input("편집할 위치를 다시 입력하세요(취소: 0):"))
                                    placeIsOK = True
                                except ValueError:
                                    pass

                        if place == 0:
                            print("취소되었습니다.")
                            # actionSelectIsOK = True
                        elif place == 3:
                            editIsOK = viewModel.update(self.id, place, "")
                            print("변경되었습니다")
                        elif place == 6:
                            day = input("반복할 요일을 입력하세요:")
                            week_interval = input("몇 주를 주기로 반복할 지 입력하세요:")
                            due = input("반복을 마칠 날짜를 입력하세요:")
                            editIsOK = viewModel.update(self.id, place, [day, week_interval, due])
                            if editIsOK:
                                print("완료됐습니다")
                            else:
                                print("다시 입력해주세요")
                        elif place <= 7:
                            content = input("내용을 입력하세요:")
                            editIsOK = viewModel.update(self.id, place, content)
                            if editIsOK:
                                print("완료됐습니다")
                                # self.loadView()
                                # actionSelectIsOK = True
                            else:
                                print("다시 입력해주세요")
                        else:
                            print("다시 입력해주세요")
                elif button == "2":
                    del viewModel
                    actionSelectIsOK = True
                    reload = False
                elif button == "3":
                    actionSelectIsOK = True
                    reload = False
                else:
                    print("다시 입력해주세요")

# view = TodoDetailView(TodoViewModel("name", 1, True, 100, 0, 0, "f"))
# view.loadView()

# class Program:
#     def __init__(self):
#         self.view = TodoDetailView()
#         self.suvView = []
#
#         self.done = False
#     def main(self):
#         while(not self.done):
#             if len(self.suvView) == 0:
#                 self.view.loadView()
#             else:
#                 self.suvView[-1].loadView()
#
# APP
# Scene
# ViewController