import time

from .cgroup import *
from .mountpoint import *
from .subsys import *

_cgroupFSType = "cgroup"
_cgroupSubsysCPU = "cpu"
_cgroupSubsysCPUAcct = "cpuacct"
_cgroupSubsysCPUSet = "cpuset"
_cgroupSubsysMemory = "memory"

_cgroupMemoryLimitInBytesParam = "memory.limit_in_bytes"
_cgroupMemoryUsageInBytesParam = "memory.usage_in_bytes"
_cgroupCPUCFSQuotaUsParam = "cpu.cfs_quota_us"
_cgroupCPUCFSPeriodUsParam = "cpu.cfs_period_us"
_cgroupCPUACCTUsageUsParam = "cpuacct.usage"

_procPathCGroup = "/proc/self/cgroup"
_procPathMountInfo = "/proc/self/mountinfo"


class CGroups:
    def __init__(self):
        self.cgroups = {}

    def cpu_quota(self):
        if _cgroupSubsysCPU not in self.cgroups:
            return -1, False

        cpu_group = self.cgroups[_cgroupSubsysCPU]

        cfs_quota_us = cpu_group.read_int(_cgroupCPUCFSQuotaUsParam)
        cfs_period_us = cpu_group.read_int(_cgroupCPUCFSPeriodUsParam)

        if cfs_period_us == -1 or cfs_quota_us == -1:
            return -1, False

        return float(cfs_quota_us) / float(cfs_period_us), True

    def cpu_usage(self):
        if _cgroupSubsysCPUAcct not in self.cgroups:
            return -1, False

        cpu_group = self.cgroups[_cgroupSubsysCPUAcct]

        start_time = time.time()
        cpu_usage_start = cpu_group.read_int(_cgroupCPUACCTUsageUsParam)

        if cpu_usage_start == -1:
            return -1, False

        time.sleep(0.1)

        cpu_usage_end = cpu_group.read_int(_cgroupCPUACCTUsageUsParam)
        end_time = time.time()

        cpu_usage = (cpu_usage_end - cpu_usage_start) / ((end_time - start_time) * 1000000000)

        return cpu_usage, True

    def memory_limit(self):
        if _cgroupSubsysMemory not in self.cgroups:
            return -1, False

        memory_group = self.cgroups[_cgroupSubsysMemory]

        memory_limit = memory_group.read_int(_cgroupMemoryLimitInBytesParam)

        if memory_limit == -1:
            return -1, False

        return memory_limit, True

    def memory_usage(self):
        if _cgroupSubsysMemory not in self.cgroups:
            return -1, False

        memory_group = self.cgroups[_cgroupSubsysMemory]

        memory_usage = memory_group.read_int(_cgroupMemoryUsageInBytesParam)

        if memory_usage == -1:
            return -1, False

        return memory_usage, True

    def __setitem__(self, key, value):
        self.cgroups[key] = value

    def __getitem__(self, item):
        return self.cgroups[item]


def parse_mountinfo_into_cgroups(cgroup_subsystems, cgroups):
    def wrap_parse_mountinfo(mount_point):
        if mount_point.fs_type != _cgroupFSType:
            return None

        for opt in mount_point.super_options:
            if opt not in cgroup_subsystems:
                continue

            subsys = cgroup_subsystems[opt]
            cgroup_path = mount_point.translate(subsys.name)
            if cgroup_path == "":
                continue

            cgroups[opt] = new_cgroup(cgroup_path)

    return wrap_parse_mountinfo


def new_cgroups(proc_path_mount_info, proc_path_cgroup):
    cgroup_subsystems = parse_cgroup_subsystems(proc_path_cgroup)

    cgroups = CGroups()

    parse_mountinfo(proc_path_mount_info, parse_mountinfo_into_cgroups(cgroup_subsystems, cgroups))

    return cgroups


def new_cgroups_for_current_process():
    return new_cgroups(_procPathMountInfo, _procPathCGroup)
