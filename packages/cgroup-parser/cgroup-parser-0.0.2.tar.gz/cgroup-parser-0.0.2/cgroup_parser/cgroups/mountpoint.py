import os

_mountInfoSep = " "
_mountInfoOptsSep = ","
_mountInfoOptionalFieldsSep = "-"

# MountInfoFirstHalf:
_miFieldIDMountID = 0
_miFieldIDParentID = 1
_miFieldIDDeviceID = 2
_miFieldIDRoot = 3
_miFieldIDMountPoint = 4
_miFieldIDOptions = 5
_miFieldIDOptionalFields = 6

_miFieldCountFirstHalf = 7

# MountInfoSecondHalf:
_miFieldOffsetFSType = 0
_miFieldOffsetMountSource = 1
_miFieldOffsetSuperOptions = 2

_miFieldCountSecondHalf = 3

_miFieldCountMin = _miFieldCountFirstHalf + _miFieldCountSecondHalf


class MountPoint:
    def __init__(self, mount_id=0,
                 parent_id=0,
                 device_id="",
                 root="",
                 mount_point="",
                 options=None,
                 optional_fields=None,
                 fs_type="",
                 mount_source="",
                 super_options=None):
        self.mount_id = mount_id
        self.parent_id = parent_id
        self.device_id = device_id
        self.root = root
        self.mount_point = mount_point
        self.options = options
        self.optional_fields = optional_fields
        self.fs_type = fs_type
        self.mount_source = mount_source
        self.super_options = super_options

    def translate(self, abs_path):
        rel_path = os.path.relpath(abs_path, self.root)

        if rel_path == ".." or rel_path.startswith("../"):
            return ""

        return os.path.join(self.mount_point, rel_path)


def new_mount_point_from_line(line):
    fields = line.split(_mountInfoSep)

    if len(fields) < _miFieldCountMin:
        return None

    mount_id = 0
    parent_id = 0
    try:
        mount_id = int(fields[_miFieldIDMountID])
        parent_id = int(fields[_miFieldIDParentID])
    except:
        return None

    for i, field in enumerate(fields[_miFieldIDOptionalFields:]):
        if field == _mountInfoOptionalFieldsSep:
            fs_type_start = _miFieldIDOptionalFields + i + 1

            if len(fields) != fs_type_start + _miFieldCountSecondHalf:
                return None

            miFieldIDFSType = _miFieldOffsetFSType + fs_type_start
            miFieldIDMountSource = _miFieldOffsetMountSource + fs_type_start
            miFieldIDSuperOptions = _miFieldOffsetSuperOptions + fs_type_start

            return MountPoint(mount_id=mount_id,
                              parent_id=parent_id,
                              device_id=fields[_miFieldIDDeviceID],
                              root=fields[_miFieldIDRoot],
                              mount_point=fields[_miFieldIDMountPoint],
                              options=fields[_miFieldIDOptions].split(_mountInfoOptsSep),
                              optional_fields=fields[_miFieldIDOptionalFields:(fs_type_start - 1)],
                              fs_type=fields[miFieldIDFSType],
                              mount_source=fields[miFieldIDMountSource],
                              super_options=fields[miFieldIDSuperOptions].split(_mountInfoOptsSep))


def parse_mountinfo(proc_path_mount_info, parse_mountinfo_into_cgroups):
    with open(proc_path_mount_info, mode='r') as file:
        for line in file.readlines():
            mount_point = new_mount_point_from_line(line.strip())
            if mount_point is None:
                continue
            parse_mountinfo_into_cgroups(mount_point)
