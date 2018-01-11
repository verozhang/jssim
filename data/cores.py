from enum import Enum


class CoreStatus(Enum):
    VACANT = 0
    OCCUPIED = 1
#   End CoreStatus


class Core(object):

    def __init__(self, node_name, core_name):
        self.node_name = node_name
        self.core_name = core_name
        self.status = CoreStatus.VACANT
        self.job = None
        self.events = []
        return
    #   End __init__

    def occupy(self, job):
        #   Occupying an occupied core is illegal.
        if self.status == CoreStatus.OCCUPIED:
            raise CoreOccupyError
        self.status = CoreStatus.OCCUPIED
        self.job = job
        return
    #   End occupy

    def release(self):
        if self.status == CoreStatus.VACANT:
            raise CoreReleaseError
        self.status = CoreStatus.VACANT
        self.job = None
        return
    #   End release

    def output(self):
        print("Core", self.node_name, self.core_name)
        for event in self.events:
            event.output()
        return
    #   End output
#   End Core


class CoreList(list):

    pass
#   End CoreList


class CoreEventType(Enum):
    OCCUPY = 0
    RELEASE = 1
#   End CoreEventType


class CoreEvent(object):

    def __init__(self, core, time):
        self.core = core
        self.time = time
        return
    #   End __init__
#   End CoreEvent


class CoreEventOccupy(CoreEvent):

    def __init__(self, core, job, time):
        super().__init__(core, time)
        self.job = job
        self.type = CoreEventType.OCCUPY
        return
    #   End __init__

    def output(self):
        print("Core", self.core.node_name, self.core.core_name, "is occupied by", self.job.job_id, "on", self.time)
    #   End output
#   End CoreEventOccupy


class CoreEventRelease(CoreEvent):

    def __init__(self, core, time):
        super().__init__(core, time)
        self.type = CoreEventType.RELEASE
        return
    #   End __init__

    def output(self):
        print("Core", self.core.node_name, self.core.core_name, "is released on", self.time)
    #   End output
#   End CoreEventRelease


class CoreError(Exception):
    pass


class CoreOccupyError(CoreError):
    pass


class CoreReleaseError(CoreError):
    pass


class CoreListError(Exception):
    pass


class CoreListEmptyPopError(CoreListError):
    pass


class CoreListIllegalPopError(CoreListError):
    pass
