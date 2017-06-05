from data.cores import *
from data.queues import *
from data.jobs import *
from data.users import *
from data.resourcepool import *
import gl


def init_job(file_name):
    #   Read from file.
    in_file = open(file_name, 'r')
    #   Read each line.
    for line in in_file.readlines():
        line = line.split()

        job_id = int(line[0])
        for job in gl.jobs_all.jobs:
            if job.job_id == job_id:
                raise JobDuplicateIDError

        user_id = int(line[1])
        #   Search for user.
        for user in gl.users_all.users:
            #   Found user.
            if user.user_id == user_id:
                current_user = user
                break
        # Cannot find. Create new user.
        else:
            current_user = User(user_id)
            gl.users_all.push(current_user)

        submit_time = int(line[2])
        start_time = int(line[3])
        stop_time = int(line[4])
        run_time = int(line[5])
        num_processors = int(line[6])
        job = Job(job_id, current_user, submit_time, start_time, stop_time, run_time, num_processors)
        gl.jobs_all.push(job)
        current_user.job_list.push(job)

    #   Push all jobs into queue_waiting.
    for job in gl.jobs_all.jobs:
        gl.queue_waiting.job_list.push(job)
    gl.queue_waiting.sort_by_submit_time()

    print("Job properties successfully imported from file.")
    return
#   End init_job


def init_resource():
    #   Init cores.
    node_num = int(input("Please input node number."))
    core_num = int(input("Please input core number."))
    gl.total_node_num = node_num
    gl.total_core_num = core_num * node_num

    for node_name in range(node_num):
        node = Node(node_name, gl.total_core_num)
        gl.resource_all.node_list_append(node)

    gl.resource_all.count_cores()

    return
#   End init_resource


def init_queue():
    #   Init pend queues.
    while True:
        queue_mode = input("Please select queue mode."
                           "1 for single-queue mode,"
                           "2 for semi-auto queue generating,"
                           "3 for manual queue generating.")
        while queue_mode != '1' and queue_mode != '2' and queue_mode != '3':
            print("Input error, please retry.")

        #   Single queue mode:
        #   Only 1 queue. All jobs will be pushed to this queue.
        #   All resources will be used only by this queue.
        if queue_mode == '1':
            queue_name = "Queue_Pending1"
            queue = PendQueue(queue_name)
            queue.set_core_num(1, gl.total_core_num)
            gl.queues_pending.append(queue)
            queue.resource_pools.resource_list_append(gl.resource_all)
            break

        #   Semi-auto mode:
        #   Set interval points of core numbers.
        #   All jobs will be sent to queues according to cores needed.
        #   Higher priority for queues of larger jobs.
        elif queue_mode == '2':
            pass




'''
    queue_num = int(input("Please input number of queues."))
    gl.queue_num = queue_num
    while queue_num <= 0:
        print("Queue number must be positive integer, please input again")
        queue_num = int(input("Please input number of queues."))

    #   Semi-auto queue settings:
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
                queue.set_core_num(min_core_num, gl.total_node_num * gl.total_core_num)
            queue.set_priority(queue_num - i)
            gl.queues_pending.append(queue)
            queue.resource_pools.resource_list.append(gl.resource_all)
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
'''
    return
#   End init_queue
