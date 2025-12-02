from adapters.in_memory_task_repository import InMemoryTaskRepository
from adapters.cli.controller import TaskCLIController
from core.use_cases import (
    AddTaskUseCase,
    ListTasksUseCase,
    CompleteTaskUseCase,
)


def main() -> None:
    # 永続化の実装（Adapter）
    task_repository = InMemoryTaskRepository()

    # ユースケース（ドメイン中心のアプリケーションサービス）
    add_task_use_case = AddTaskUseCase(task_repository)
    list_tasks_use_case = ListTasksUseCase(task_repository)
    complete_task_use_case = CompleteTaskUseCase(task_repository)

    # CLI コントローラ（UI Adapter）
    controller = TaskCLIController(
        add_task_use_case=add_task_use_case,
        list_tasks_use_case=list_tasks_use_case,
        complete_task_use_case=complete_task_use_case,
    )

    # CLI ループ開始
    controller.run()


if __name__ == "__main__":
    main()