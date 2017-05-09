from data.cores import CoreList
from data.jobs import JobList
from data.users import UserList
from data.queues import Queue

VERSION = "1.2"

node_num = 1
core_num = 1

start_time = 0
finish_time = float("inf")
current_time = start_time

users_all = UserList()

jobs_all = JobList()

cores_all = CoreList()
cores_vacant = CoreList()

queue_waiting = Queue("Queue_Waiting")
queue_arrived = Queue("Queue_Arrived")
queue_running = Queue("Queue_Running")
queue_finished = Queue("Queue_Finished")
queue_abandoned = Queue("Queue_Abandoned")

queue_num = 1
queues_pending = []
