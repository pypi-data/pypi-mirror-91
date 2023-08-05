import os


class CGroup:
    def __init__(self, path=""):
        self.path = path

    def path(self):
        return self.path

    def param_path(self, param):
        return os.path.join(self.path, param)

    def read_first_line(self, param):
        first_line = ""
        with open(self.param_path(param), mode='r') as file:
            first_line = file.readline().strip()
        return first_line

    def read_int(self, param):
        result = -1
        try:
            text = self.read_first_line(param)
            result = int(text)
        except:
            pass
        return result


def new_cgroup(path):
    return CGroup(path=path)
