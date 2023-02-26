from django.db import models


class Task:
    def __init__(self, id, task_time):
        self._id = id
        self._status = False
        self._task_time = task_time
        self._count_down = task_time

    def __str__(self) -> str:
        return f" task: {self._id}"


class Work:
    def __init__(self, id) -> None:
        self._id = id
        self._status = False
        self._is_completed = False
        self._tasks = None
        self._actual_machine = 0

    def __str__(self) -> str:
        output = f"work with id: {self._id}, completed: {self._status}"
        output += f" current task {self._tasks[self._actual_machine]._count_down}"
        return output


class Machine:
    def __init__(self, id):
        self._id = id
        self._status = False
        self._work_id = 0
        self._count_down = 0

    def __str__(self) -> str:
        return f"status {self._status}"
