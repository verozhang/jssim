from data.jobs import JobList
from data.users import UserList
from data.queues import Queue
from data.resourcepool import *

VERSION = "1.2"

total_node_num = 1
each_core_num = 1
total_core_num = 1

start_time = 0
finish_time = float("inf")
current_time = start_time

users_all = UserList()

jobs_all = JobList()

queue_waiting = Queue("Queue_Waiting")
queue_arrived = Queue("Queue_Arrived")
queue_running = Queue("Queue_Running")
queue_finished = Queue("Queue_Finished")
queue_abandoned = Queue("Queue_Abandoned")

queue_num = 1
queues_pending = []

resource_all = ResourcePool()

# Following stats are used for evaluation
cpu_occupation_status = {}  # Record occupation status on each time point.
cpu_occupation_rate = {}

total_waiting_job_num = {}
total_waiting_core_num = {}

sum_wait_time = 0
sum_run_time = 0
sum_cpu_time = 0

max_wait_time = 0
max_run_time = 0
max_cpu_time = 0
max_response_ratio = 0
