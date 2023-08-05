import cgroup_parser


def test_interface():
    cgroup_parser.get_max_procs()
    cgroup_parser.get_cpu_usage()
    cgroup_parser.get_memory_limit()
    cgroup_parser.get_memory_usage()
