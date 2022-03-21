#!/usr/bin/env python3

# 1、引入bcc 库的BPF 模块
from  bcc  import BPF
# 2、调用BPF() 加载BPF 源码
b = BPF(src_file="hello.c")

# 3、将BPF程序挂载到 内核探针 kprobe  内核函数do_sys_openat2(),触发函数时执行钩子函数  hello_word
b.attach_kprobe(event="do_sys_openat2", fn_name="hello_world")
# 4) read and print /sys/kernel/debug/tracing/trace_pipe
b.trace_print()

