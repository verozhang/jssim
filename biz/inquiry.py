import gl


def inquiry():
    for core in gl.cores_all.cores:
        for event in core.events:
            event.output()

    for job in gl.jobs_all.jobs:
        for event in job.events:
            event.output()

    menu_help = ("\n"
                 "H - This menu.\n"
                 "S - Status and settings of current system.\n"
                 "R - Status of current simulation.\n"
                 "J - Status of jobs.\n"
                 "C - Status of cores.\n"
                 "U - Status of users.\n"
                 "A - About.\n"
                 "Q - Quit program.\n")

    while True:
        command = input("Please input command.\n")
        # Print help list.
        if command == 'h' or command == 'H':
            print(menu_help)

        # Print system status: Node & core num and queue settings.
        elif command == 's' or command == 'S':
            print("System node number:", gl.node_num)
            print("Core number of each node:", gl.core_num)
            print("Queue settings:")
            print("Queue number:", gl.queue_num)
            for queue in gl.queues_pending:
                print("Queue name:", queue.name)
                print("Priority:", queue.priority)
                print("Available core num:", queue.min_core_num, "to", queue.max_core_num)

        # Print running status: time and job count.
        elif command == 'r' or command == 'R':
            print("Start time:", gl.start_time)
            print("Finish time:", gl.finish_time)
            print("Finished jobs:", gl.queue_finished.get_length())
            print("Running jobs:", gl.queue_running.get_length())
            print("Abandoned jobs:", gl.queue_abandoned.get_length())

        # Print job status.
        elif command == 'j' or command == 'J':
            job_ask = input("Please input job ID.\n")
            for job in gl.jobs_all.jobs:
                if job_ask == str(job.job_id):
                    job.output()
                    break
            else:
                print("Job", job_ask, "not found.")

        # Print core status.
        elif command == 'c' or command == 'C':
            node_ask = input("Please input node No.\n")
            core_ask = input("Please input core No.\n")
            for core in gl.cores_all.cores:
                if node_ask == str(core.node_name) and core_ask == str(core.core_name):
                    core.output()
                    break
            else:
                print("Core", node_ask, core_ask, "not found")
                #   Search method should be re-determined.

        # Print user status.
        elif command == 'u' or command == 'U':
            user_ask = input("Please input user name.\n")
            for user in gl.users_all.users:
                if user_ask == str(user.user_id):
                    user.output()
                    break
            else:
                print("User", user_ask, "not found.")

        elif command == 't' or command == 'T':
            pass

        # Print ABOUT info.
        elif command == 'a' or command == 'A':
            print("Super-Computing Simulator Ver.", gl.VERSION)
            print("Author: Yi-Chi \"Vero\" Zhang@SCC-USTC.")
            print("Mailto: vero at mail dot ustc dot edu dot cn")
            print("Supervisor: Dr. Yu Shen@SCC-USTC.")
            print("Mailto: shenyu at ustc dot edu dot cn")

        # Quit program.
        elif command == 'q' or command == 'Q':
            break

        # Wrong input handle.
        else:
            print("This command does not exist or is under development, please retry.")
            continue
    return
#   End inquiry
