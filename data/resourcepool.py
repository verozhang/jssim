from enum import Enum


class Node(object):

    def __init__(self, node_name, core_num):
        self.node_name = node_name
        self.core_num = core_num
        self.core_used = 0
        self.status = {}
        self.events = []
        return
    #   End __init__

    def occupy(self, job, core_usage):
        if not self.status[job]:
            self.status[job] = core_usage
        else:
            self.status[job] += core_usage

        self.core_used += core_usage
        return
    #   End occupy

    def release(self, job):
        self.core_used -= self.status[job]
        del (self.status[job])
        return
    #   End release

    def try_occupy(self, job, core_usage):
        if self.core_num - self.core_used < core_usage:
            return False
        if job in self.status[job]:
            return False
        return True
    #   End try_occupy
#   End Node


class NodeEventType(Enum):
    OCCUPY = 0
    RELEASE = 1
#   End NodeEventType


class ResourcePool(object):

    def __init__(self):
        self.node_list = []
        self.cores_available = 0
        self.priority = 0
        return
    #   End __init__

    def count_cores(self):
        for node in self.node_list:
            self.cores_available += node.core_num
        return
    #   End count_cores

    def node_list_append(self, node):
        if node in self.node_list:
            raise Exception
        else:
            self.node_list.append(node)
            self.cores_available += node.core_num
        return
    #   End node_list_append

    def node_list_remove(self, node):
        if node not in self.node_list:
            raise Exception
        else:
            self.node_list.remove(node)
            self.cores_available -= node.core_num
        return
    #   End node_list_remove
#   End ResourcePool


class ResourceEventType(Enum):
    OCCUPY = 0
    RELEASE = 1
#   End ResourceEventType


class ResourceEvent(object):

    def __init__(self, node, time):
        self.node = node
        self.time = time
        return
    #   End __init__
#   End ResourceEvent


class ResourceEventOccupy(ResourceEvent):

    def __init__(self, node, time, job):
        super().__init__(node, time)
        self.job = job
        self.type = ResourceEventType.OCCUPY
        return
    #   End __init__

    def output(self):
        print("")
        return
    #   End output
#   End ResourceEventOccupy


class ResourceEventRelease(ResourceEvent):

    def __init__(self, node, time, job):
        super().__init__(node, time)
        self.job = job
        self.type = ResourceEventType.RELEASE
        return
    #   End __init__

    def output(self):
        print("")
        return
    #   End output
#   End ResourceEventRelease
