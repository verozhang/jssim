from data.cores import *
from data.queues import *
import gl


def system_init():
    #   Initialise cores.
    finish_time = int(input("Please input finish time."))
    gl.finish_time = finish_time

    node_num = int(input("Please input node number."))
    core_num = int(input("Please input core number."))
    gl.node_num = node_num
    gl.core_num = core_num

    for node_name in range(node_num):
        for core_name in range(core_num):
            core = Core(node_name, core_name)
            gl.cores_all.push(core)
            gl.cores_vacant.push(core)

    #   Initialise Jobs.
    for job in gl.jobs_all.jobs:
        gl.queue_waiting.job_list.push(job)

    #   Initialise queues.
    queue_num = int(input("Please input number of queues."))
    gl.queue_num = queue_num
    while queue_num <= 0:
        print("Queue number must be positive integer, please input again")
        queue_num = int(input("Please input number of queues."))

    for i in range(queue_num):
        queue_name = "Queue_Pending" + str(i + 1)
        queue = PendQueue(queue_name)
        gl.queues_pending.append(queue)

    return
