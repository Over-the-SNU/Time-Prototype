from TodoViewModel import TodoViewModel
class TodoDetailView:
    def __init__(self, viewModel: TodoViewModel):
        self.viewModel = viewModel
    def loadView(self):
        print(f"Todo: {self.viewModel.name} (중요도: {self.viewModel.importance})")
        if self.viewModel.done:
            print("완료됨")
        else:
            print(f"진행도: {self.viewModel.progress}")

        print(f"시간: {self.viewModel.date}")
        print(f"반복: {self.viewModel.repeat}")
        print(f"메모: {self.viewModel.content}")
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
                    print(f"1. Todo: {self.viewModel.name}")
                    print(f"2. 중요도: {self.viewModel.importance}")
                    print(f"3. 완료: {self.viewModel.done}")
                    print(f"4. 진행도: {self.viewModel.progress}")
                    print(f"5. 시간: {self.viewModel.date}")
                    print(f"6. 반복: {self.viewModel.repeat}")
                    print(f"7. 메모: {self.viewModel.content}")
                    place = int(input("편집할 위치를 정하세요(취소: 0):"))
                    if not place == 3:
                        content = input("내용을 입력하세요:")
                        editIsOK = self.viewModel.modify(place, content)
                        if editIsOK:
                            print("완료됐습니다")
                            self.loadView()
                            actionSelectIsOK = True
                        else:
                            print("다시 입력해주세요")
            elif button == "2":
                del self.viewModel
                actionSelectIsOK = True
            elif button == "3":
                actionSelectIsOK = True
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