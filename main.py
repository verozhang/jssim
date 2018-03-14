#!  usr/bin/python3
#   encoding : utf-8

from biz.systeminit import *
from biz.run import *
from biz.inquiry import *

if __name__ == '__main__':
    print("Thank you for using JSSim Ver.", gl.VERSION)
    print("Initializing simulation.")
    init_job()
    init_resource()
    init_queue()

    simulate()
    inquiry()
