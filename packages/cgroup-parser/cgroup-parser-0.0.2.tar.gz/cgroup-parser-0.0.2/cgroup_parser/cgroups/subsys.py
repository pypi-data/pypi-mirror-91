_cgroupSep = ":"
_cgroupSubsysSep = ","

_csFieldIDID = 0
_csFieldIDSubsystems = 1
_csFieldIDName = 2
_csFieldCount = 3


class CGroupSubsys:
    def __init__(self, proc_id=0, subsystems=None, name=""):
        self.id = proc_id
        self.subsystems = subsystems
        self.name = name


def new_cgroup_subsys_from_line(line):
    fields = line.split(_cgroupSep)

    if len(fields) != _csFieldCount:
        return None

    proc_id = 0
    try:
        proc_id = int(fields[_csFieldIDID])
    except:
        return None

    return CGroupSubsys(proc_id=proc_id, subsystems=fields[_csFieldIDSubsystems].split(_cgroupSubsysSep),
                        name=fields[_csFieldIDName])


def parse_cgroup_subsystems(proc_path_cgroup):
    subsystems = {}
    with open(proc_path_cgroup, mode='r') as file:
        for line in file.readlines():
            cgroup = new_cgroup_subsys_from_line(line.strip())
            if cgroup is None:
                continue
            for subsys in cgroup.subsystems:
                subsystems[subsys] = cgroup
    return subsystems
