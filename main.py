#!  usr/bin/python3
#   encoding : utf-8

from biz.systeminit import *
from biz.input import *
from biz.run import *
from biz.inquiry import *

if __name__ == '__main__':
    input_file("input")
    system_init()
    simulate()
    inquiry()
