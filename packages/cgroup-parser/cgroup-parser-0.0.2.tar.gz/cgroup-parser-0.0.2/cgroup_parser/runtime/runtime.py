from ..cgroups import CGroups

GLOBAL_CGROUP: CGroups = None


class CGroupStatus:
    CGroupUndefined = 1

    CPUQuotaUsed = 2
    CPUQuotaMinUsed = 3

    CPUUsageUsed = 4

    MemoryLimitUsed = 5

    MemoryUsageUsed = 6
