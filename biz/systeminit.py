from data.cores import *
from data.queues import *
import gl


def system_init():
    #   Initialise cores.
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
    queue_mode = input("Please select queue mode, 1 for semi-auto, 2 for manual.")
    while queue_mode != '1' and queue_mode != '2':
        print("Input error, please input again.")
        queue_mode = input("Please select queue mode, 1 for semi-auto, 2 for manual.")

    queue_num = int(input("Please input number of queues."))
    gl.queue_num = queue_num
    while queue_num <= 0:
        print("Queue number must be positive integer, please input again")
        queue_num = int(input("Please input number of queues."))

    #   Semi-auto queue settings: set interval points of core numbers.
    #   All jobs will be sent to queues according to cores needed.
    #   Higher priority for queues of larger jobs.
    if queue_mode == '1':
        min_core_num = 1
        max_core_num = 1
        for i in range(queue_num):
            queue_name = "Queue_Pending" + str(i + 1)
            queue = PendQueue(queue_name)
            if i != (queue_num - 1):
                max_core_num = int(input("Please input maximum core number for queue " + queue_name))
                queue.set_core_num(min_core_num, max_core_num)
            else:
                queue.set_core_num(min_core_num, node_num * core_num)
            queue.set_priority(queue_num - i)
            gl.queues_pending.append(queue)
            min_core_num = max_core_num + 1

    #   Manual mode: all settings input by keyboard.
    elif queue_mode == '2':
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
