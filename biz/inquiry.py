from matplotlib.pyplot import plot, show
import gl


def inquiry():

    for job in gl.jobs_all:
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
            print("System total node number:", gl.total_core_num)

        elif command == 'q' or command == 'Q':
            print("Queue number:", gl.queue_num)
            for queue in gl.queues_pending:
                print("Queue name:", queue.name)
                print("Priority:", queue.priority)
                print("Available core num:", queue.core_num_floor, "to", queue.core_num_ceiling)
                print("Total job number:", queue.total_job_num)
                print("Total core number:", queue.total_core_num)
                print("Total wait time:", queue.total_wait_time)
                print("Average wait time:", queue.total_wait_time / queue.total_job_num)
                print("Total run time:", queue.total_run_time)
                print("Average run time:", queue.total_run_time / queue.total_job_num)
                print("Total CPU time:", queue.total_cpu_time)
                print("Average CPU time:", queue.total_cpu_time / queue.total_job_num)
                print("Average response ratio:", (queue.total_wait_time + queue.total_run_time) / queue.total_run_time)
                print("Max wait time:", queue.max_wait_time)
                print("Max run time:", queue.max_run_time)
                print("Max CPU time:", queue.max_cpu_time)
                print("Max response ratio:", queue.max_response_ratio)

        # Print running status: time and job count.
        elif command == 'r' or command == 'R':
            print("Start time:", gl.start_time)
            print("Finish time:", gl.finish_time)
            print("Finished jobs:", gl.queue_finished.get_length())
            # print("Running jobs:", gl.queue_running.get_length())
            print("Abandoned jobs:", gl.queue_abandoned.get_length())

        elif command == 'e' or command == 'E':
            # Times
            avg_run_time = gl.sum_run_time / gl.queue_finished.get_length()
            avg_wait_time = gl.sum_wait_time / gl.queue_finished.get_length()
            avg_cpu_time = gl.sum_cpu_time / gl.queue_finished.get_length()

            print("Total wait time:", gl.sum_wait_time)
            print("Average wait time:", avg_wait_time)
            print("Total run time:", gl.sum_run_time)
            print("Average run time:", avg_run_time)
            print("Total turnaround time:", gl.sum_wait_time + gl.sum_run_time)
            print("Average turnaround time:", avg_wait_time + avg_run_time)

            print("Average response ratio:", (gl.sum_wait_time + gl.sum_run_time) / gl.sum_run_time )

            print("Total cpu time:", gl.sum_cpu_time)
            print("Average cpu time per job:", avg_cpu_time)

            print("Max wait time:", gl.max_wait_time)
            print("Max run time:", gl.max_run_time)
            print("Max CPU time:", gl.max_cpu_time)
            print("Max response ratio:", gl.max_response_ratio)

            # Occupation rate
            is_output = input("Export occupation rate status?\n")
            if is_output == 'y' or is_output == 'Y':

                interval = int(input("Please input sampling interval."))
                if interval <= 0:
                    interval = int(input("Wrong input, please try again."))
                print("Exporting, please wait.\n")

                time_list = []
                stat_list = []
                rate_list = []

                out_file = open('output_status', 'w')
                for item in gl.cpu_occupation_status:
                    if item % interval == 0:
                        out_file.write(str(item))
                        time_list.append(str(item))
                        out_file.write(' ')
                        out_file.write(str(gl.cpu_occupation_status[item]))
                        stat_list.append(gl.cpu_occupation_status[item])
                        out_file.write('\n')
                out_file.close()

                out_file = open('output_rate', 'w')
                for item in gl.cpu_occupation_rate:
                    if item % interval == 0:
                        out_file.write(str(item))
                        out_file.write(' ')
                        out_file.write(str(gl.cpu_occupation_rate[item]))
                        rate_list.append(gl.cpu_occupation_rate[item])
                        out_file.write('\n')
                out_file.close()

                plot(time_list, stat_list)
                show()

                print("Export successful.\n")

        # Print job status.
        elif command == 'j' or command == 'J':
            job_ask = input("Please input job ID.\n")
            for job in gl.jobs_all:
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
            print("Mail: vero@mail.ustc.edu.cn")
            print("Supervisor: Dr. Yu Shen@SCC-USTC")
            print("Mail: shenyu@ustc.edu.cn")

        # Quit program.
        elif command == 'x' or command == 'X':
            break

        # Wrong input handle.
        else:
            print("This command does not exist or is under development, please retry.")

    return
#   End inquiry
