import platform
import math

from ..cgroups import *
from . import runtime

if "linux" in platform.platform().lower():
    class MessageType:
        cpu_quota = 1
        cpu_usage = 2
        memory_limit = 3
        memory_usage = 4


    def init_global_cgroups():
        if runtime.GLOBAL_CGROUP is None:
            runtime.GLOBAL_CGROUP = new_cgroups_for_current_process()


    def cpu_quota_to_max_procs(min_value):
        quota, defined = read_cgroup_message(MessageType.cpu_quota)
        if not defined:
            return -1, runtime.CGroupStatus.CGroupUndefined

        max_procs = int(math.floor(quota))
        if min_value > 0 and max_procs < min_value:
            return min_value, runtime.CGroupStatus.CPUQuotaMinUsed

        return max_procs, runtime.CGroupStatus.CPUQuotaUsed


    def cpu_quota_to_usage():
        # 会阻塞100ms
        usage, defined = read_cgroup_message(MessageType.cpu_usage)
        if not defined:
            return -1, runtime.CGroupStatus.CGroupUndefined

        return usage, runtime.CGroupStatus.CPUUsageUsed


    def memory_quota_to_limit():
        limit, defined = read_cgroup_message(MessageType.memory_limit)
        if not defined:
            return -1, runtime.CGroupStatus.CGroupUndefined

        return limit, runtime.CGroupStatus.MemoryLimitUsed


    def memory_quota_to_usage():
        usage, defined = read_cgroup_message(MessageType.memory_usage)
        if not defined:
            return -1, runtime.CGroupStatus.CGroupUndefined

        return usage, runtime.CGroupStatus.MemoryUsageUsed


    def read_cgroup_message(msg_type):
        init_global_cgroups()

        if runtime.GLOBAL_CGROUP is None:
            return -1, False

        if msg_type == MessageType.cpu_quota:
            data, defined = runtime.GLOBAL_CGROUP.cpu_quota()
        elif msg_type == MessageType.cpu_usage:
            data, defined = runtime.GLOBAL_CGROUP.cpu_usage()
        elif msg_type == MessageType.memory_limit:
            data, defined = runtime.GLOBAL_CGROUP.memory_limit()
        elif msg_type == MessageType.memory_usage:
            data, defined = runtime.GLOBAL_CGROUP.memory_usage()
        else:
            data, defined = -1, False

        return data, True
