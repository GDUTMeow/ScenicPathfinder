import sys
import os

def get_workdir() -> str:
    # 编译后
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    # 源码运行时
    return os.getcwd()