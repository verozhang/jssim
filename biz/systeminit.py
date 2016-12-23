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
    gl.queue_waiting.sort_by_submit_time()

    #   Initialise queues.
    queue_num = int(input("Please input number of queues."))
    gl.queue_num = queue_num
    while queue_num <= 0:
        print("Queue number must be positive integer, please input again")
        queue_num = int(input("Please input number of queues."))

    for i in range(queue_num):
        queue_name = "Queue_Pending" + str(i + 1)
        queue = PendQueue(queue_name)
        min_core_num = int(input("Please input minimum core number for queue " + queue_name))
        max_core_num = int(input("Please input maximum core number for queue " + queue_name))
        queue.set_core_num(min_core_num, max_core_num)
        priority = int(input("Please input priority for queue " + queue_name))
        queue.set_priority(priority)
        gl.queues_pending.append(queue)

    return
