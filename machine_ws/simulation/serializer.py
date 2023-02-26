from simulation.models import Machine, Work

def work_serializer(work:Work):
    work_dict = {
        "id":work._id,
        "status": work._status,
        "is_completed" : work._is_completed,
        "actual_machine" : work._actual_machine
    }
    return work_dict

def machine_serializer(machine:Machine):
    machine_dict = {
        "id" : machine._id,
        "status" : machine._status,
        "work_id" : machine._work_id,
        "count_down" : machine._count_down
    }
    return machine_dict
