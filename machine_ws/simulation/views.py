from django.shortcuts import render
from simulation.models import Work, Machine, Task
import pandas as pd


def index(request):
    if request.method == "GET":
        return render(request,'create_task.html')
    tasks_id = list(filter(lambda x: x.startswith('task') ,request.POST))
    tasks = []
    for task in tasks_id:
        if '' not in dict(request.POST)[task]:
            tasks.append(dict(request.POST)[task])
        else:
            tasks.append(['0' for i in dict(request.POST)[task]])
    works_init, machines_init = instace_works_machines(tasks)
    clock,df = simulation(works_init,machines_init)
    return render(request, 'index.html',{"clock": clock,"df":df})


def simulation(works,machines):
    register = pd.DataFrame({
        "Machine":[],"Current_work":[],
        "Count_down":[],"Time (secs)":[],
        "Status":[]})
    clock = 0
    while True:
        works_init, machines_init = search_task(works, machines)
        clock += 1
        for machine in machines_init:
            register = register.append(
                    pd.Series(["M"+str(machine._id),
                               "W"+str(machine._work_id),
                               str(machine._count_down)+' Secs',
                               str(clock),machine._status],
                              index=['Machine','Current_work',
                                     'Count_down','Time (secs)',
                                     'Status']),ignore_index=True)
        if check_end(works_init):
            break
    return clock,register.to_html(index=False)


def instace_works_machines(works):
    n_machines = len(works[0])
    machines_init = []
    works_init = []
    for i in range(n_machines):
        machines_init.append(Machine(i))
    for i,work in enumerate(works):
        new_work = Work(i)
        new_work._tasks = []
        for j,task in enumerate(work):
            new_work._tasks.append(Task(j,int(task)))
        works_init.append(new_work)
    return (works_init, machines_init)


def verify_non_zero(work: Work,  machine_count: int):
    for i in range(machine_count):
        if work._tasks[work._actual_machine]._count_down <= 0:
            if work._actual_machine < machine_count:
                work._actual_machine += 1
            else:
                work._is_completed = True
    return work


def search_task(works: list[Work], machines: list[Machine]):
    for work in works:
        work = verify_non_zero(work, len(machines)-1)
        if all([work._is_completed == False,
                work._status == False,
                machines[work._actual_machine]._status == False]):
            machines[work._actual_machine], work = set_work(machines[work._actual_machine], work)
    for work in works:
        if work._status:
            execute_task(work, machines[work._actual_machine], len(machines)-1)
    return (works, machines)


def execute_task(work: Work, machine: Machine, machine_count: int):
    if machine._count_down > 0:
        machine._count_down -= 1
        work._tasks[work._actual_machine]._count_down -= 1
    end_work(work, machine, machine_count)


def end_work(work: Work, machine: Machine, machine_count: int):
    if machine._count_down <= 0:
        machine._status = False
        work._status = False
        if work._actual_machine == machine_count:
            work._is_completed = True
        else:
            work._actual_machine += 1


def set_work(machine: Machine, work: Work):
    machine._work_id = work._id
    machine._status = True
    machine._count_down = work._tasks[work._actual_machine]._task_time
    work._status = True
    return (machine, work)


def check_end(works: list[Work]):
    inactive_machines = list(filter(lambda x: x._is_completed, works))
    return len(inactive_machines) == len(works)
