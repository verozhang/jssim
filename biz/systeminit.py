import json
from data.queues import *
from data.jobs import *
from data.users import *
from data.resourcepool import *
import gl


def init_job():
    # Read from file.
    while True:
        try:
            in_file_name = input("Please input name of input file.\n")
            in_file = open(in_file_name, 'r')
        except FileNotFoundError:
            print("File not found. "
                  "Please try again.\n")
        else:
            break

    # Read each line.
    for line in in_file.readlines():
        line = line.split()

        try:
            line[0] and line[1] and line[2] and line[3] and line[4] and line[5] and line[6]
        except IndexError:
            print("Job input error: "
                  "Wrong input in file. "
                  "Terminating.")
            raise JobInputError

        job_id = int(line[0])
        for job in gl.jobs_all:
            if job.job_id == job_id:
                print("Job input error: "
                      "Duplicate job ID for job", job_id,
                      "Terminating.")
                raise JobDuplicateIDError

        user_id = int(line[1])
        # Search for user.
        for user in gl.users_all.users:
            # Found user.
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
        gl.jobs_all.append(job)
        current_user.job_list.append(job)

    in_file.close()

    # Push all jobs into queue_waiting.
    for job in gl.jobs_all:
        gl.queue_waiting.job_list.append(job)
    gl.queue_waiting.sort_by_submit_time()

    print("Job properties successfully imported from file.")
    return
# End init_job


def init_job_from_json():
    # Read from a json. Further work needed here.
    # See lsb.acct-Handler.
    while True:
        try:
            in_json_name = input("Please input name of json file.\n")
            in_json = json.load(in_json_name)
        except FileNotFoundError:
            print("File not found. "
                  "Please try again.\n")
        else:
            break

    for item in in_json:
        pass
    return


def init_resource():
    # Init cores.
    while True:
        try:
            node_num = int(input("Please input node number.\n"))
            core_num = int(input("Please input core number.\n"))
        except ValueError:
            print("Node num & core num must be positive integer.\n"
                  "Please try again.\n")
        else:
            break
    
    gl.total_node_num = node_num
    gl.each_core_num = core_num
    gl.total_core_num = core_num * node_num

    for node_name in range(node_num):
        node = Node(node_name, gl.each_core_num)
        gl.resource_all.node_list_append(node)

    gl.resource_all.count_cores()

    return
# End init_resource


def init_queue():
    # Init pend queues.
    while True:
        queue_mode = input("Please select queue mode.\n"
                           "1 for single-queue mode,\n"
                           "2 for semi-auto queue generating,\n"
                           "3 for manual queue generating.\n")
        while queue_mode != '1' and queue_mode != '2' and queue_mode != '3':
            print("Input error, please retry.")
            break

        # Single queue mode:
        # Only 1 queue. All jobs will be pushed to this queue.
        # All resources will be used only by this queue.
        if queue_mode == '1':
            queue_name = "Queue_Pending"
            queue = PendQueue(queue_name)
            queue.set_core_num(1, gl.total_core_num)
            queue.resource_pools.resource_list_append(gl.resource_all)
            gl.queues_pending.append(queue)
            break

        # Semi-auto mode:
        # Set interval points of core numbers.
        # All jobs will be sent to queues according to cores needed.
        # Higher priority for queues of larger jobs.
        elif queue_mode == '2':
            current_min_core_num = 1
            while True:
                gl.queue_num = int(input("Please input queue number."))
                if gl.queue_num > 1:
                    break
                else:
                    print("Queue num must be more than 1, please retry.")

            for i in range(gl.queue_num):
                queue_name = "Queue_Pending" + str(i + 1)
                queue = PendQueue(queue_name)

                if i != gl.queue_num - 1:
                    # Not the last queue, max core num input by user.
                    current_max_core_num = int(input("Please input maximum core num for queue " + queue_name))
                else:
                    # Last queue, max core num is total core num.
                    current_max_core_num = gl.total_core_num
                queue.set_core_num(current_min_core_num, current_max_core_num)

                queue.set_priority(i + 1)

                queue.core_num_running_limit = int(input("Please input maximum core num for queue "
                                                         + queue_name
                                                         + " to use running.\n"))

                gl.queues_pending.append(queue)
                queue.resource_pools.resource_list_append(gl.resource_all)
                current_min_core_num = current_max_core_num + 1

            break

        elif queue_mode == '3':
            while True:
                gl.queue_num = int(input("Please input queue number."))
                if gl.queue_num > 1:
                    break
                else:
                    print("Queue num must be more than 1, please retry.\n")

            for i in range(gl.queue_num):
                queue_name = "Queue_Pending" + str(i + 1)
                queue = PendQueue(queue_name)

                queue.min_core_num = int(input("Please input min core num for queue" + queue_name))
                queue.max_core_num = int(input("Please input max core num for queue" + queue_name))
                queue.priority = int(input("Please input priority for queue" + queue_name))

                gl.queues_pending.append(queue)
                queue.resource_pools.resource_list_append(gl.resource_all)
            break
    return
# End init_queue
