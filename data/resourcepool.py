from data.cores import *


class ResourcePool(object):

    def __init__(self, name):
        self.name = name
        self.vacancy = len(self.core_list.cores)
        self.core_list = CoreList()
        return
