from data.jobs import JobList
from enum import Enum


class Queue(object):
    def __init__(self, name):
        self.name = name
        self.job_list = JobList()
        self.events = []
        return
    #   End __init__

    def sort_by_submit_time(self):
        self.job_list.jobs.sort(key=lambda x: x.submit_time, reverse=False)
        return
    #   End sort_by_submit_time

    def sort_by_start_time(self):
        self.job_list.jobs.sort(key=lambda x: x.start_time, reverse=False)
        return
    #   End sort_by_start_time

    def sort_by_finish_time(self):
        self.job_list.jobs.sort(key=lambda x: x.real_start_time + x.run_time, reverse=False)
        return
    #   End sort_by_finish_time

    def load(self, job):
        self.job_list.push(job)
        return
    #   End load

    def unload(self, job):
        self.job_list.pop(job)
        return
    #   End unload

    def try_has_job(self):
        return bool(self.job_list.jobs)
    #   End try_has_job

    def get_length(self):
        return self.job_list.get_length()
    #   End get_length

    def get_head(self):
        return self.job_list.get_head()
    #   End get_head
#   End Queue


class QueueBackFillStatus(Enum):
    NoBackFill = 0
    BackFill = 1


class PendQueue(Queue):

    def __init__(self, name):
        super().__init__(name)
        self.min_core_num = 0
        self.max_core_num = float("inf")
        self.priority = 50
        self.resource_pools = []

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

        return
    #   End __init__

    def resource_pool_append(self, resource):
        if resource in self.resource_pools:
            raise Exception
        else:
            self.resource_pools.append(resource)
            self.resource_pools.sort(key=lambda x: x.priority, reverse=True)
            return
    #   End resource_pool_append

    def resource_pool_remove(self, resource):
        if resource not in self.resource_pools:
            raise Exception
        else:
            self.resource_pools.remove(resource)
            return
    #   End resource_pool_remove

    def set_core_num(self, minimum, maximum):
        self.min_core_num = minimum
        self.max_core_num = maximum
        return
    #   End set_core_num

    def set_priority(self, priority):
        self.priority = priority
        return
    #   End set_priority

    def try_suitable(self, job):
        if self.min_core_num <= job.num_processors <= self.max_core_num:
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

    def try_running_limit(self, job):
        if self.job_num_running + 1 <= self.job_num_running_limit:
            if self.core_num_pending + job.num_processors <= self.core_num_running_limit:
                return True
            else:
                return False
        else:
            return False
    #   End try_running_limit

    def try_user_pending_limit(self, job):
        #   User not in lists.
        if (job.user not in self.user_job_num_pending) and (job.user not in self.user_core_num_pending):
            return True
        #   User in one list but not another, must be a bug.
        elif (job.user in self.user_job_num_pending) != (job.user in self.user_core_num_pending):
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

    def try_user_running_limit(self, job):
        #   User not in lists.
        if (job.user not in self.user_job_num_running) and (job.user not in self.user_core_num_running):
            return True
        elif (job.user not in self.user_job_num_running) != (job.user not in self.user_core_num_running):
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
