from enum import Enum


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


class Work:
    def __init__(self, id) -> None:
        """

        Args:
            id (): int
        """
        self._id = id
        self._status = False
        self._is_completed = False
        self._tasks = []
        self._actual_machine = 0

    def __str__(self) -> str:
        output = f"work with id: {self._id}, completed: {self._status}"
        output += f" current task {self._tasks[self._actual_machine]._count_down}"
        return output

    def verify_non_zero(self):
        """Check if the current task of the work is not zero

        Returns: None
            
        """
        while self._tasks[self._actual_machine]._count_down < 1 and self._is_completed == False:
            if self._actual_machine < len(self._tasks)-1:
                self._actual_machine += 1
            else:
                self._is_completed = True
                return


class Machine:
    def __init__(self, id):
        """Machine init

        Args:
            id (): int
        """
        self._id = id
        self._status = False
        self._events = Enum('Event',['STARTED','INACTIVE','RUNNING','FINISHED'])
        self._current_event = self._events.INACTIVE
        self._work_id = 0
        self._count_down = 0

    def __str__(self) -> str:
        return f"status {self._status}"

    def execute_task(self,task:Task):
        """if the _count_down is higher than zero reduce one second of the
        task and the machine

        Args:
            task: Task
        """
        if self._count_down > 0:
            self._count_down -= 1
            self._current_event = self._events.RUNNING
            task._count_down -= 1
