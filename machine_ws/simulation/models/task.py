class Task:
    def __init__(self, id, task_time):
        """Task init

        Args:
            id (): int 
            task_time (): int 
        """
        self._id = id
        self._status = False
        self._task_time = task_time
        self._count_down = task_time

    def __str__(self) -> str:
        return f" task: {self._id}"
