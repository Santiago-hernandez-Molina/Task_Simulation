from enum import Enum

class Machine:
    def __init__(self, id):
        """Machine init

        Args:
            id (int)
        """
        self._id = id
        self._status = False
        self._events = Enum('Event',['STARTED','INACTIVE','RUNNING','FINISHED'])
        self._current_event = self._events.INACTIVE
        self._task = None
        self._work_id = 0
        self._count_down = 0

    def __str__(self) -> str:
        return f"status {self._status}"

    def execute_task(self):
        """if the _count_down is higher than zero reduce one second of the
        task and the machine

        Args:
            task (Task)
        """
        if self._count_down > 0:
            self._count_down -= 1
            self._current_event = self._events.RUNNING
            self._task._count_down -= 1
        self.end_work()

    def end_work(self):
        if self._count_down < 1:
            self._status = False
            self._current_event = self._events.FINISHED
