from numpy import int64
import pandas as pd
from simulation.models import Work, Task, Machine

class Simulation:
    def __init__(self):
        self._works = []
        self._machines = []
        self._clock = 0
        self._register = pd.DataFrame({
            "Machine":pd.Series(dtype='str'),"Current_work":pd.Series(dtype='str'),
            "Count_down":pd.Series(dtype='int'),"Time (secs)":pd.Series(dtype='int'),
            "Status":pd.Series(dtype='bool'),"Event":[]})

    def run(self):
        while  not self.check_end():
            self.search_task()
            self.get_registers()
            self.execute_machines()
            self._clock += 1
        return self._clock,self._register.to_html(index=False)


    def get_registers(self):
        """ this method saves the information in a DataFrame """
        for machine in self._machines:
            self._register = pd.concat([
                self._register,
                pd.DataFrame({
                    "Machine":["M"+str(machine._id)],"Current_work":["W"+str(machine._work_id)],
                    "Count_down":[int64(machine._count_down)],"Time (secs)":[int64(self._clock)],
                    "Status":[machine._status],"Event":[machine._current_event]})])


    def instace_works_machines(self,works):
        """

        Args:
            works (): list[list[int]]
        """
        for i in range(len(works[0])):
            self._machines.append(Machine(i))
        for i,work in enumerate(works):
            new_work = Work(i)
            for j,task in enumerate(work):
                new_work._tasks.append(Task(j,int(task)))
            self._works.append(new_work)


    def search_task(self):
        """ Find avaliables works to be executed in a machine """
        for work in self._works:
            work.verify_non_zero()
            if all([work._is_completed == False,
                    work._status == False,
                    self._machines[work._actual_machine]._status == False]):
                self._machines[work._actual_machine], work = self.set_work_to_machine(
                        self._machines[work._actual_machine], work)


    def set_work_to_machine(self,machine: Machine, work: Work):
        """

        Args:
            machine: Machine
            work: Work

        Returns: tuple(machine, work)
            
        """
        machine._work_id = work._id
        machine._current_event = machine._events.STARTED
        machine._status = True
        machine._count_down = work._tasks[work._actual_machine]._task_time
        work._status = True
        return (machine, work)


    def execute_machines(self):
        for machine in self._machines:
            if machine._status:
                work = self._works[machine._work_id]
                machine.execute_task(work._tasks[work._actual_machine])
                self.end_work(work, machine)



    def end_work(self,work: Work, machine: Machine):
        """It checks if count_down is zero

        Args:
            work: Work
            machine: Machine
        """
        if machine._count_down < 1:
            machine._status = False
            work._status = False
            machine._current_event = machine._events.FINISHED


    def check_end(self):
        """It checks is all works are completed

        Returns: boolean
            
        """
        inactive_machines = list(filter(lambda x: x._is_completed, self._works))
        end = len(inactive_machines) == len(self._works)
        if end:
            self._clock -= 1 
        return end
