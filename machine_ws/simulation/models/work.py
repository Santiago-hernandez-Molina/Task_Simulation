from simulation.models.task import Task 

class Work:
    def __init__(self, id) -> None:
        """
        Args:
            id (): int
        """
        self._id = id
        self._is_completed = False
        self._tasks:list[Task] = []
        self._current_machine = 0

    def __str__(self) -> str:
        output = f"work with id: {self._id}, completed: {self._is_completed}"
        output += f" current task {self._tasks[self._current_machine]._count_down}"
        return output

    def verify_non_zero(self):
        """Check if the current task of the work is not zero
        Returns: None
        """
        while self._tasks[self._current_machine]._count_down < 1 and self._is_completed == False:
            if self._current_machine < len(self._tasks)-1:
                self._current_machine += 1
            else:
                self._is_completed = True
                return

    def get_avaliable_task(self):
        self.verify_non_zero()
        if all([self._is_completed == False, 
                self._tasks[self._current_machine]._status == False]):
            return self._tasks[self._current_machine]
        return None


