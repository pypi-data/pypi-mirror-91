# Python解析cgroup（支持容器）
1. 获取CPU核数
2. 获取CPU使用率
3. 获取内存限量
4. 获取内存占用量

```
import cgroup_parser
cgroup_parser.get_max_procs()
cgroup_parser.get_cpu_usage()
cgroup_parser.get_memory_limit()
cgroup_parser.get_memory_usage()
```
