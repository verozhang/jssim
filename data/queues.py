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


class PendQueue(Queue):

    def __init__(self, name):
        super().__init__(name)
        self.min_core_num = 0
        self.max_core_num = float("inf")
        self.priority = 50
        self.user_job_num = {}
        return
    #   End __init__

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
