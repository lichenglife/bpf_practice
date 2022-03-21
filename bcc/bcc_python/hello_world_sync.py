#!/usr/bin/python
# Copyright (c) PLUMgrid, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")

# run in project examples directory with:
# sudo ./hello_world.py"
# see trace_fields.py for a longer example

from  bcc  import  BPF

# BCC 宏定义
BPF(text='int kprobe__sys_sync(void *ctx){bpf_trace_printk("hello world! \\n"); return 0 ;}').trace_print()
 