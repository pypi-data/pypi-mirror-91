import platform

from .runtime import *

if "linux" not in platform.platform().lower():
    def cpu_quota_to_max_procs(min_value):
        return -1, CGroupStatus.CGroupUndefined


    def cpu_quota_to_usage():
        return -1, CGroupStatus.CGroupUndefined


    def memory_quota_to_limit():
        return -1, CGroupStatus.CGroupUndefined


    def memory_quota_to_usage():
        return -1, CGroupStatus.CGroupUndefined
