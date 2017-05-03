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


class NodeGroup(object):

    def __init__(self, group_name):
        self.group_name = group_name
        self.nodes = []
        return
    #   End __init__
#   End NodeGroup
