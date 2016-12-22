from data.jobs import JobList


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
        return
    #   End __init__

    def set_core_num(self, min, max):
        self.min_core_num = min
        self.max_core_num = max
        return
    #   End set_core_num

    def set_priority(self, priority):
        self.priority = priority
        return
    #   End set_priority

    def try_suitable(self, job):
        if job.num_processors >= self.min_core_num and job.num_processors <= self.max_core_num:
            return True
        else:
            return False
#   End PendQueue


class QueueError(Exception):
    pass
