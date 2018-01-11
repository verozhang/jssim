from data.jobs import JobList
from data.resourcepool import ResourceGroup
from enum import Enum


class Queue(object):
    def __init__(self, name):
        self.name = name
        self.job_list = JobList()
        self.events = []
        return
    #   End __init__

    def sort_by_submit_time(self):
        self.job_list.sort(key=lambda x: x.submit_time, reverse=False)
        return
    #   End sort_by_submit_time

    def sort_by_start_time(self):
        self.job_list.sort(key=lambda x: x.start_time, reverse=False)
        return
    #   End sort_by_start_time

    def sort_by_finish_time(self):
        self.job_list.sort(key=lambda x: x.real_start_time + x.run_time, reverse=False)
        return
    #   End sort_by_finish_time

    def load(self, job):
        self.job_list.append(job)
        return
    #   End load

    def unload(self, job):
        self.job_list.remove(job)
        return
    #   End unload

    def try_has_job(self):
        return bool(self.job_list)
    #   End try_has_job

    def get_length(self):
        return self.job_list.__len__()
    #   End get_length

    def get_core_length(self):
        return self.job_list.core_length()
    #   End get_core_length

    def get_head(self):
        return self.job_list[0]
    #   End get_head
#   End Queue


class PendQueue(Queue):

    def __init__(self, name):
        super().__init__(name)
        self.core_num_floor = 0
        self.core_num_ceiling = float("inf")
        self.run_time_floor = 0
        self.run_time_ceiling = float("inf")
        self.priority = 0
        self.resource_pools = ResourceGroup()

        self.job_num_pending = 0                    # Num of jobs pending through this queue.
        self.job_num_pending_limit = float("inf")     # Num of jobs a queue can have pending.
        self.core_num_pending = 0                   # Num of cores asking for.
        self.core_num_pending_limit = float("inf")    # Num of cores a queue can have asking for.

        self.user_job_num_pending = {}
        self.user_job_num_pending_limit = float("inf")  # Num of jobs a user can have pending on this queue.
        self.user_core_num_pending = {}
        self.user_core_num_pending_limit = float("inf")

        self.job_num_running = 0                    # Num of jobs running through this queue.
        self.job_num_running_limit = float("inf")
        self.core_num_running = 0
        self.core_num_running_limit = float("inf")
        self.cputime_running = 0
        self.cputime_running_limit = float("inf")

        self.user_job_num_running = {}
        self.user_job_num_running_limit = float("inf")
        self.user_core_num_running = {}
        self.user_core_num_running_limit = float("inf")
        self.user_cputime_running = {}
        self.user_cputime_running_limit = float("inf")

        self.total_job_num = 0
        self.total_core_num = 0
        self.total_wait_time = 0
        self.total_run_time = 0
        self.total_cpu_time = 0
        self.max_wait_time = 0
        self.max_run_time = 0
        self.max_cpu_time = 0
        self.max_response_ratio = 0

        return
    #   End __init__

    def resource_pool_append(self, resource):
        if resource in self.resource_pools:
            print("Resource pool append error: "
                  "Resource already in pool. "
                  "Terminating.")
            raise QueueError
        else:
            self.resource_pools.resource_list.append(resource)
            self.resource_pools.resource_list.sort(key=lambda x: x.priority, reverse=True)
            return
    #   End resource_pool_append

    def resource_pool_remove(self, resource):
        if resource not in self.resource_pools:
            print("Resource pool remove error: "
                  "Resource not in pool. "
                  "Terminating.")
            raise QueueError
        else:
            self.resource_pools.resource_list.remove(resource)
            return
    #   End resource_pool_remove

    def get_resource(self):
        return max(lambda x: self.resource_pools.cores_available)
    #   End get)resource

    def set_core_num(self, minimum, maximum):
        self.core_num_floor = minimum
        self.core_num_ceiling = maximum
        return
    #   End set_core_num

    def set_run_time(self, minimum, maximum):
        self.run_time_floor = minimum
        self.run_time_ceiling = maximum
        return
    #   End set_run_time

    def set_priority(self, priority):
        self.priority = priority
        return
    #   End set_priority

    def try_suitable(self, job):
        if self.core_num_floor <= job.num_processors <= self.core_num_ceiling:
            return True
        else:
            return False
    #   End try_suitable

    def try_pending_limit(self, job):
        if self.job_num_pending + 1 <= self.job_num_pending_limit:
            if self.core_num_pending + job.num_processors <= self.core_num_pending_limit:
                return True
            else:
                return False
        else:
            return False
    #   End try_pending_limit

    def try_user_pending_limit(self, job):
        #   User not in lists.
        if (job.user not in self.user_job_num_pending) and (job.user not in self.user_core_num_pending):
            return True
        #   User in one list but not another, must be a bug.
        elif (job.user in self.user_job_num_pending) != (job.user in self.user_core_num_pending):
            print("Try user pending limit error: "
                  "User in job num list but not in core num list, or vice versa. "
                  "Terminating.")
            raise QueueError
        #   User in both lists.
        elif self.user_job_num_pending[job.user] + 1 <= self.user_job_num_pending_limit:
            if self.user_core_num_pending[job.user] + job.num_processors <= self.user_core_num_pending_limit:
                return True
            else:
                return False
        else:
            return False
    #   End try_user_pending_limit

    def try_running_limit(self, job):
        if self.job_num_running + 1 <= self.job_num_running_limit:
            if self.core_num_pending + job.num_processors <= self.core_num_running_limit:
                return True
            else:
                return False
        else:
            return False
    #   End try_running_limit

    def try_user_running_limit(self, job):
        #   User not in lists.
        if (job.user not in self.user_job_num_running) and (job.user not in self.user_core_num_running):
            return True
        elif (job.user not in self.user_job_num_running) != (job.user not in self.user_core_num_running):
            print("Try user running limit error: "
                  "User in job num list but not in core num list, or vice versa. "
                  "Terminating.")
            raise QueueError
        elif self.user_job_num_running[job.user] + 1 <= self.user_job_num_running_limit:
            if self.user_core_num_running[job.user] + job.num_processors <= self.user_core_num_running_limit:
                return True
            else:
                return False
        else:
            return False
    #   End try_user_running_limit
#   End PendQueue


class QueueEventType(Enum):
    Load = 0
    Unload = 1
#   End QueueEventType


class QueueEvent(object):

    def __init__(self, queue, job, time):
        self.queue = queue
        self.job = job
        self.time = time
        return
    #   End __init__
#   End QueueEvent


class QueueEventLoad(QueueEvent):

    def output(self):
        print("Queue", self.queue, "loads job", self.job, "on", self.time)
        return
    #   End output
#   End QueueEventLoad


class QueueEventUnload(QueueEvent):

    def output(self):
        print("Queue", self.queue, "unloads job", self.job, "on", self.time)
        return
    #   End output
#   End QueueEventUnload


class QueueError(Exception):
    pass
