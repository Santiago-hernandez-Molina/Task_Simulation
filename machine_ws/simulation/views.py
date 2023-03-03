from django.shortcuts import render
from simulation.utils import Simulation


def index(request):
    if request.method == "GET":
        return render(request,'create_task.html')
    tasks = get_task_from_post(request.POST)
    simulation = Simulation()
    simulation.instace_works_machines(tasks)
    clock,df = simulation.run()
    return render(request, 'index.html',{"clock": clock,"df":df})


def get_task_from_post(post_task):
    """This method receive a post request and gets from it every task,
    later return a matrix with them"""
    tasks_id = list(filter(lambda x: x.startswith('task'),post_task))
    tasks = []
    for task in tasks_id:
        print(dict(post_task)[task])
        if '' not in dict(post_task)[task]:
            tasks.append(dict(post_task)[task])
        else:
            tasks.append(['0' for i in dict(post_task)[task]])
    return tasks



