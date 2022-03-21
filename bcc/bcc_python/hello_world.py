#!/usr/bin/python
# Copyright (c) PLUMgrid, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")

# run in project examples directory with:
# sudo ./hello_world.py"
# see trace_fields.py for a longer example

from  bcc  import  BPF

# BCC 宏定义
BPF(text='int kprobe__sys_clone(void *ctx){bpf_trace_printk("hello world! \\n"); return 0 ;}').trace_print()

# 涉及的语法
""" 
1、text='' 表示定义了一个BPF内联程序，程序用C实现。
2、kprobe__sys_clone  是内核函数跟踪点，即这个BPF程序要监控的系统调用函数，同时可以换成其他的系统调用kprobe__sys_sync、kprobe__sys_close
3、void *ctx 函数参数
4、bpf_trace_printk  内核函数，输出打印，同时建议使用BPF_PERF_OUTPUT()
5、.trace_print() 是bcc的程序，读取trace_pipe中数据并输出
6、

"""
 