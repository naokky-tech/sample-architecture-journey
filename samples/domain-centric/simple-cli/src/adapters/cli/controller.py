from __future__ import annotations

from core.use_cases import (
    AddTaskUseCase,
    ListTasksUseCase,
    CompleteTaskUseCase,
)


class TaskCLIController:
    """CLI からユースケースを呼び出すコントローラ。

    - 入力のパース・簡単なバリデーション
    - ユースケースの実行
    - 結果の整形・表示

    など、「UI まわりの責務」を担当します。
    """

    def __init__(
        self,
        add_task_use_case: AddTaskUseCase,
        list_tasks_use_case: ListTasksUseCase,
        complete_task_use_case: CompleteTaskUseCase,
    ) -> None:
        self._add_task_use_case = add_task_use_case
        self._list_tasks_use_case = list_tasks_use_case
        self._complete_task_use_case = complete_task_use_case

    def run(self) -> None:
        while True:
            self._print_menu()
            choice = input("番号を選んでください: ").strip()

            if choice == "1":
                self._handle_add_task()
            elif choice == "2":
                self._handle_list_tasks()
            elif choice == "3":
                self._handle_complete_task()
            elif choice == "0":
                print("終了します。")
                return
            else:
                print("不正な入力です。もう一度お試しください。")

            print()  # 区切りの空行

    def _print_menu(self) -> None:
        print("==== タスク管理 (ドメイン中心アーキテクチャ版) ====")
        print("1. タスクを追加する")
        print("2. タスク一覧を表示する")
        print("3. タスクを完了にする")
        print("0. 終了する")

    def _handle_add_task(self) -> None:
        title = input("タスク名を入力してください: ").strip()
        if not title:
            print("タスク名は空にはできません。")
            return

        task = self._add_task_use_case.execute(title=title)
        print(f"タスクを追加しました (id={task.id}, title={task.title})")

    def _handle_list_tasks(self) -> None:
        tasks = self._list_tasks_use_case.execute()
        if not tasks:
            print("登録されているタスクはありません。")
            return

        print("現在のタスク一覧:")
        for task in tasks:
            status = "✅ 完了" if task.is_completed else "⬜ 未完了"
            print(f"- [{status}] {task.id}: {task.title}")

    def _handle_complete_task(self) -> None:
        raw_id = input("完了にするタスクのIDを入力してください: ").strip()

        if not raw_id.isdigit():
            print("ID は数値で入力してください。")
            return

        task_id = int(raw_id)
        task = self._complete_task_use_case.execute(task_id=task_id)

        if task is None:
            print(f"ID={task_id} のタスクが見つかりませんでした。")
            return

        print(f"タスクを完了にしました (id={task.id}, title={task.title})")