import pandas as pd
from simulation.models import Work, Task, Machine

class Simulation:
    def __init__(self) -> None:
        self._works = []
        self._machines = []
        self._clock = 0
        self._register = pd.DataFrame({
            "Machine":[],"Current_work":[],
            "Count_down":[],"Time (secs)":[],
            "Status":[],"Event":[]})

    def run(self):
        while  not self.check_end():
            self.search_task()
            self.get_registers()
            self.execute_task()
            self._clock += 1
        return self._clock,self._register.to_html(index=False)


    def get_registers(self):
        for machine in self._machines:
            self._register = self._register.append(
                    pd.Series(["M"+str(machine._id),
                               "W"+str(machine._work_id),
                               str(machine._count_down)+' Secs',
                               str(self._clock),machine._status,
                               machine._current_event],
                              index=['Machine','Current_work',
                                     'Count_down','Time (secs)',
                                     'Status','Event']),ignore_index=True)


    def instace_works_machines(self,works):
        for i in range(len(works[0])):
            self._machines.append(Machine(i))
        for i,work in enumerate(works):
            new_work = Work(i)
            new_work._tasks = []
            for j,task in enumerate(work):
                new_work._tasks.append(Task(j,int(task)))
            self._works.append(new_work)


    def search_task(self):
        for work in self._works:
            work.verify_non_zero()
            if all([work._is_completed == False,
                    work._status == False,
                    self._machines[work._actual_machine]._status == False]):
                self._machines[work._actual_machine], work = self.set_work(
                        self._machines[work._actual_machine], work)


    def execute_task(self):
        for work in self._works:
            if work._status:
                machine = self._machines[work._actual_machine]
                if machine._count_down > 0:
                    machine._count_down -= 1
                    machine._current_event = machine._events.RUNNING
                    work._tasks[work._actual_machine]._count_down -= 1
                self.end_work(work, machine)


    def end_work(self,work: Work, machine: Machine):
        if machine._count_down < 1:
            machine._status = False
            work._status = False
            machine._current_event = machine._events.FINISHED
            work.verify_non_zero()


    def set_work(self,machine: Machine, work: Work):
        machine._work_id = work._id
        machine._current_event = machine._events.STARTED
        machine._status = True
        machine._count_down = work._tasks[work._actual_machine]._task_time
        work._status = True
        return (machine, work)


    def check_end(self):
        inactive_machines = list(filter(lambda x: x._is_completed, self._works))
        end = len(inactive_machines) == len(self._works)
        if end:
            self.get_registers()
        return end
