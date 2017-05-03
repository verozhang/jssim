import gl
from biz.input import *
from biz.systeminit import *


def startup():
    print("Thank you for using JSSim Ver.", gl.VERSION)
    input_file("input")
    system_init()
