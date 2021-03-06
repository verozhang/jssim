from enum import Enum


class JobStatus(Enum):
    WAITING = 0     # Have not arrived at the server.
    ARRIVED = 1     # Arrived at the server, still waiting for start time.
    PENDING = 2     # On queue, waiting for resources.
    RUNNING = 3     # Running.
    FINISHED = 4    # Finished running and released its resources.

    ABANDONED = -1  # Cannot be started due to finish time.
#   End JobStatus


class Job(object):

    def __init__(self, job_id, user, submit_time, start_time, stop_time, run_time, num_processors):
        self.job_id = job_id
        self.user = user
        self.submit_time = submit_time   # Time this job reaches server
        if start_time == 0:              # Time user allows this job to start. 0 means run when arrive.
            self.start_time = submit_time
        else:
            self.start_time = start_time
        if stop_time == 0:            # Time this job become useless. Stop even it is not finished. 0 means do not stop.
            self.stop_time = float("inf")
        else:
            self.stop_time = stop_time
        self.run_time = run_time          # Time this job needed to run. Assume it is correct.
        self.real_start_time = 0          # Time when this job actually starts.
        self.real_end_time = 0            # Time when this job actually ends.
        self.real_run_time = 0            # Time this job actually cost.
        self.real_wait_time = 0           # Time this job is on queue waiting for resources.
        self.turnaround_time = 0          # Wait time + run time.
        self.response_ratio = 0           # Turnaround time / run time ratio.
        self.num_processors = num_processors
        self.status = JobStatus.WAITING

        self.queue_from = None
        self.node_usage = {}
        self.resource_pool_usage = None

        self.events = []
        return
    #   End __init__

    def try_arrive(self, current_time):
        #   Test if work has arrived.
        if current_time < self.submit_time:
            return False
        else:
            return True
    #   End try_arrive

    def try_run(self, current_time):
        #   Test if the user has permitted the work to start.
        if current_time < self.start_time:
            return False
        else:
            return True
    #   End try_run

    def try_finish(self, current_time):
        #   Test if the work has finished.
        if current_time < self.real_start_time + self.run_time:
            return False
        else:
            return True
    #   End try_finish

    def output(self):
        print("Job", self.job_id, "is submitted by user", self.user.user_id)
        for event in self.events:
            event.output()
        print("Wait time for job", self.job_id, ":", self.real_wait_time)
        return
    #   End output
#   End Job


class JobList(list):

    def __init__(self):
        super().__init__()
        self.core_length = 0
        return
    #   End __init__

    def append(self, job):
        super().append(job)
        self.core_length += job.num_processors
        return
    #   End append

    def remove(self, job):
        super().remove(job)
        self.core_length -= job.num_processors
        return
    #   End remove

#   End JobList


class JobEventType(Enum):
    ARRIVE = 0      # Job arrive at the server.
    PEND = 1        # Job reaches start time, put on queue and starts asking for resources.
    RUN = 2         # Job starts running.
    FINISH = 3      # Job finishes running.

    ABANDON = -1    # Job is abandoned.
    REQUEUE = -2    # Job cannot be added to queue and is requeued.
#   End JobEventType


class JobEvent(object):

    def __init__(self, job, time):
        self.job = job
        self.time = time
        return
    #   End __init__
#   End JobEvent


class JobEventArrive(JobEvent):

    def __init__(self, job, time):
        super().__init__(job, time)
        self.type = JobEventType.ARRIVE
        return
    #   End __init__

    def output(self):
        print("Job", self.job.job_id, "arrives on", self.time)
        return
    #   End output
#   End JobEventArrive


class JobEventPend(JobEvent):

    def __init__(self, job, queue, time):
        super().__init__(job, time)
        self.queue = queue
        self.type = JobEventType.PEND
        return
    #   End __init__

    def output(self):
        print("Job", self.job.job_id, "is put on queue", self.queue.name, "on", self.time)
        return
    #   End output
#   End JobEventPend


class JobEventRun(JobEvent):

    def __init__(self, job, time, resource):
        super().__init__(job, time)
        self.node_usage = job.node_usage
        self.resource_pool_usage = resource
        self.type = JobEventType.RUN
        return
    #   End __init__

    def output(self):
        print("Job", self.job.job_id, "start running on node")
        for node in self.node_usage:
            print(node.node_name, ":", self.node_usage[node])
        print("using resource pool", self.resource_pool_usage)
        print("on", self.time)
        return
    #   End output
#   End JobEventRun


class JobEventFinish(JobEvent):

    def __init__(self, job, time):
        super().__init__(job, time)
        self.type = JobEventType.FINISH
        return
    #   End __init__

    def output(self):
        print("Job", self.job.job_id, "finishes on", self.time)
        return
    #   End output
#   End JobEventFinish


class JobEventAbandon(JobEvent):

    def __init__(self, job, queue, time):
        super().__init__(job, time)
        self.queue = queue
        self.type = JobEventType.ABANDON
        return
    #   End __init__

    def output(self):
        print("Job", self.job.job_id, "is abandoned by queue", self.queue.name, "on", self.time)
        return
    #   End output
#   End JobEventAbandon


class JobEventRequeue(JobEvent):

    def __init__(self, job, time, time_diff):
        super().__init__(job, time)
        self.time_diff = time_diff
        self.type = JobEventType.REQUEUE
        return
    #   End __init__

    def output(self):
        print("Job", self.job.job_id, "is requeued on", self.time, "for", self.time_diff, "seconds")
        return
    #   End output
#   End JobEventRequeue


class JobError(Exception):
    pass


class JobInputError(JobError):
    pass


class JobDuplicateIDError(JobError):
    pass


class JobIllegalRunError(JobError):
    pass


class JobNoSuitableQueueError(JobError):
    pass


class JobIllegalStopError(JobError):
    pass


class JobListError(Exception):
    pass


class JobListEmptyPopError(JobListError):
    pass


class JobListIllegalPopError(JobListError):
    pass
