import os
import sys

from .runtime import *


def get_cpu_quota_to_max_procs():
    max_procs, status = cpu_quota_to_max_procs(1)

    if status == CGroupStatus.CGroupUndefined:
        # print("maxprocs: CPU quota undefined")
        return -1
    elif status == CGroupStatus.CPUQuotaMinUsed:
        # print("maxprocs: using minimum allowed MAXPROCS")
        pass
    elif status == CGroupStatus.CPUQuotaUsed:
        # print("maxprocs: determined from CPU quota")
        pass

    return max_procs


def cpu_count():
    '''
    Returns the number of CPUs in the system
    '''
    if sys.platform == 'win32':
        try:
            num = int(os.environ['NUMBER_OF_PROCESSORS'])
        except (ValueError, KeyError):
            num = 0
    elif 'bsd' in sys.platform or sys.platform == 'darwin':
        comm = '/sbin/sysctl -n hw.ncpu'
        if sys.platform == 'darwin':
            comm = '/usr' + comm
        try:
            with os.popen(comm) as p_in:
                num = int(p_in.read())
        except ValueError:
            num = 0
    else:
        try:
            num = os.sysconf('SC_NPROCESSORS_ONLN')
        except (ValueError, OSError, AttributeError):
            num = 0
    return num


# try to get get_max_procs, degraded with cpu_count
def get_max_procs():
    available_procs = cpu_count()
    maxprocs = get_cpu_quota_to_max_procs()
    if maxprocs != -1:
        available_procs = maxprocs

    available_procs = available_procs if available_procs >= 0 else 0

    return available_procs


def get_cpu_usage():
    cpu_usage, status = cpu_quota_to_usage()
    if status == CGroupStatus.CGroupUndefined:
        # print("maxprocs: CPU quota undefined")
        return -1

    return cpu_usage


def get_memory_limit():
    memory_limit, status = memory_quota_to_limit()
    if status == CGroupStatus.CGroupUndefined:
        # print("maxprocs: CPU quota undefined")
        return -1

    return memory_limit


def get_memory_usage():
    memory_usage, status = memory_quota_to_usage()
    if status == CGroupStatus.CGroupUndefined:
        # print("maxprocs: CPU quota undefined")
        return -1

    return memory_usage
