from numpy import int64
import pandas as pd
from simulation.models.work import Work
from simulation.models.task import Task
from simulation.models.machine import Machine

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
        while not self.check_end():
            self.search_task()
            self.execute_machines()
            self._clock += 1
        return self._clock,self._register.to_html(index=False)


    def get_registers(self,machine):
        """ this method saves the information in a DataFrame """
        self._register = pd.concat([
            self._register,
            pd.DataFrame({
                "Machine":["M"+str(machine._id)],"Current_work":["W"+str(machine._work_id)],
                "Count_down":[int64(machine._count_down)],"Time (secs)":[int64(self._clock)],
                "Status":[machine._status],"Event":[machine._current_event]})])


    def instace_works_machines(self,works):
        for i in range(len(works[0])):
            self._machines.append(Machine(i))
        for i,work in enumerate(works):
            new_work = Work(i)
            for j,task in enumerate(work):
                new_work._tasks.append(Task(j,int(task)))
            self._works.append(new_work)


    def search_task(self):
        for work in self._works:
            task = work.get_avaliable_task()
            if task is not None and self._machines[work._current_machine]._status ==False:
                self.set_work_to_machine(self._machines[work._current_machine], task, work._id)


    def set_work_to_machine(self,machine: Machine, task: Task, work_id: int):
        """
        Args:
            machine: Machine
            work: Work

        Returns: tuple(machine, work)

        """
        machine._task = task
        machine._current_event = machine._events.STARTED
        machine._status = True
        machine._count_down = task._task_time
        machine._work_id = work_id
        task._status = True


    def execute_machines(self):
        for machine in self._machines:
            self.get_registers(machine)
            if machine._status:
                machine.execute_task()


    def check_end(self):
        inactive_machines = list(filter(lambda x: x._is_completed, self._works))
        end = len(inactive_machines) == len(self._works)
        if end:
            self._clock -= 1
        return end
