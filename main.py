#!  usr/bin/python3
#   encoding : utf-8

from biz.systeminit import *
from biz.run import *
from biz.inquiry import *

if __name__ == '__main__':

    print("Thank you for using JSSim Ver. 1.2")

    job_flag = False
    resource_flag = False
    queue_flag = False

    while True:
        command = input("Please input command.\n"
                        "Press J to import job properties from file.\n"
                        "Press R to initialise resources.\n"
                        "Press Q to initialise queues.\n"
                        "Press C to check current system settings.\n"
                        "Press B to break initialisation and start running.\n")

        if command == 'J' or command == 'j':
            init_job("input")
            job_flag = True
            print("Job properties successfully imported from file.")

        if command == 'R' or command == 'r':
            init_resource()
            resource_flag = True

        if command == 'Q' or command == 'q':
            init_queue()
            queue_flag = True

        if command == 'C' or command == 'c':
            if resource_flag and queue_flag:
                #   Queue settings check module.#
                print("This is queue settings.")
            else:
                print("System initialisation needed before checking. "
                      "Please Try again.")

        if command == 'B' or command == 'b':
            if job_flag and resource_flag and queue_flag:
                break
            else:
                print("Error occurred. Please check input before starting.")

    simulate()
    inquiry()
