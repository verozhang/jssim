from enum import Enum


class Node(object):

    def __init__(self, node_name, core_num):
        self.node_name = node_name
        self.core_num = core_num
        self.core_vacant = core_num
        self.status = {}
        self.cputime_sum = 0
        self.events = []
        return
    #   End __init__

    def occupy(self, job, core_usage):
        if job not in self.status:
            self.status[job] = core_usage
        else:
            self.status[job] += core_usage

        self.core_vacant -= core_usage
        self.cputime_sum += core_usage * job.run_time
        return
    #   End occupy

    def release(self, job):
        self.core_vacant += self.status[job]
        del (self.status[job])
        return
    #   End release
#   End Node


class NodeEventType(Enum):
    OCCUPY = 0
    RELEASE = 1
#   End NodeEventType


class ResourcePool(object):

    def __init__(self):
        self.node_list = []
        self.cores_all = 0
        self.cores_available = 0
        self.status = {}
        self.priority = 0
        self.events = []
        return
    #   End __init__

    def count_cores(self):
        for node in self.node_list:
            self.cores_all += node.core_num
        self.cores_available = self.cores_all
        return
    #   End count_cores

    def node_list_append(self, node):
        if node in self.node_list:
            raise Exception
        else:
            self.node_list.append(node)
            self.cores_all += node.core_num
        return
    #   End node_list_append

    def node_list_remove(self, node):
        if node not in self.node_list:
            raise Exception
        else:
            self.node_list.remove(node)
            self.cores_all -= node.core_num
        return
    #   End node_list_remove

    def occupy(self, job, core_usage):
        if job not in self.status:
            self.status[job] = core_usage
        else:
            self.status[job] += core_usage

        self.cores_available -= core_usage
        return
    #   End occupy

    def release(self, job):
        self.cores_available += self.status[job]
        del (self.status[job])
        return
    #   End release
#   End ResourcePool


class ResourceGroup(object):

    def __init__(self):
        self.resource_list = []
        self.cores_all = 0
        self.cores_available = 0
        self.events = []
        return
    #   End __init__

    def count_cores(self):
        for resource in self.resource_list:
            self.cores_all += resource.count_cores()
        self.cores_available = self.cores_all
        return
    #   End count_cores

    def resource_list_append(self, resource):
        if resource in self.resource_list:
            raise Exception
        else:
            self.resource_list.append(resource)
            self.cores_all += resource.cores_all
            self.cores_available += resource.cores_all
        return
    #   End resource_list_append

    def resource_list_remove(self, resource):
        if resource not in self.resource_list:
            raise Exception
        else:
            self.resource_list.remove(resource)
            self.cores_all -= resource.cores_all
            self.cores_available -= resource.cores_available
        return
    #   End resource_list_remove
#   End ResourceGroup


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
