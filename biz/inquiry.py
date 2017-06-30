import gl


def inquiry():

    for job in gl.jobs_all.jobs:
        for event in job.events:
            event.output()

    menu_help = ("\n"
                 "H - This menu.\n"
                 "S - Status and settings of current system.\n"
                 "Q - Status of queue settings.\n"
                 "R - Status of current simulation.\n"
                 "E - Evaluation of current simulation.\n"
                 "J - Status of jobs.\n"
                 "U - Status of users.\n"
                 "A - About.\n"
                 "X - EXit program.\n")

    while True:
        command = input("Please input command.\n")
        # Print help list.
        if command == 'h' or command == 'H':
            print(menu_help)

        # Print system status: Node & core num.
        elif command == 's' or command == 'S':
            print("System node number:", gl.total_node_num)
            print("Core number of each node:", gl.each_core_num)

        elif command == 'q' or command == 'Q':
            print("Queue number:", gl.queue_num)
            for queue in gl.queues_pending:
                print("Queue name:", queue.name)
                print("Priority:", queue.priority)
                print("Available core num:", queue.min_core_num, "to", queue.max_core_num)
                print("Tobal job number:", queue.get_length())

        # Print running status: time and job count.
        elif command == 'r' or command == 'R':
            print("Start time:", gl.start_time)
            print("Finish time:", gl.finish_time)
            print("Finished jobs:", gl.queue_finished.get_length())
            print("Running jobs:", gl.queue_running.get_length())
            print("Abandoned jobs:", gl.queue_abandoned.get_length())

        elif command == 'e' or command == 'E':
            # CPU time
            sum_cpu_time = 0
            for job in gl.queue_finished.job_list.jobs:
                sum_cpu_time += job.real_run_time * job.num_processors
            avg_cpu_time = sum_cpu_time / gl.queue_finished.get_length()
            print("Total cpu time:", sum_cpu_time)
            print("Average cpu time per job:", avg_cpu_time)

            # Wait time
            sum_wait_time = 0
            for job in gl.queue_finished.job_list.jobs:
                sum_wait_time += job.real_wait_time
            avg_wait_time = sum_wait_time / gl.queue_finished.get_length()
            print("Total wait time:", sum_wait_time)
            print("Average wait time:", avg_wait_time)

            # Occupation rate
            is_output = input("Export occupation rate status?\n")
            if is_output == 'y' or is_output == 'Y':
                print("Exporting, please wait.\n")
                out_file = open('output', 'w')
                for item in gl.cpu_occupation_status:
                    out_file.write(str(item))
                    out_file.write(':')
                    out_file.write(str(gl.cpu_occupation_status[item]))
                    out_file.write('\n')
                out_file.close()
                print("Export successful.\n")

        # Print job status.
        elif command == 'j' or command == 'J':
            job_ask = input("Please input job ID.\n")
            for job in gl.jobs_all.jobs:
                if job_ask == str(job.job_id):
                    job.output()
                    break
            else:
                print("Job", job_ask, "not found.")

        # Print user status.
        elif command == 'u' or command == 'U':
            user_ask = input("Please input user name.\n")
            for user in gl.users_all.users:
                if user_ask == str(user.user_id):
                    user.output()
                    break
            else:
                print("User", user_ask, "not found.")

        # Print ABOUT info.
        elif command == 'a' or command == 'A':
            print("Job Scheduling Simulator for Super-Computers, Ver.", gl.VERSION)
            print("Author: Yi-Chi \"Vero\" Zhang@SCC-USTC.")
            print("Mail: vero at mail dot ustc dot edu dot cn")
            print("Supervisor: Dr. Yu Shen@SCC-USTC.")
            print("Mail: shenyu at ustc dot edu dot cn")

        # Quit program.
        elif command == 'x' or command == 'X':
            break

        # Wrong input handle.
        else:
            print("This command does not exist or is under development, please retry.")

    return
#   End inquiry
