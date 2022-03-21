#!/usr/bin/python
#
# sync_timing.py    Trace time between syncs.
#                   For Linux, uses BCC, eBPF. Embedded C.
#
# Written as a basic example of tracing time between events.
#
# Copyright 2016 Netflix, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")

from  __future__ import print_function
from bcc import BPF
from  bcc.utils  import  printb

#  定义 BPF 程序
b = BPF(text="""
#include <uapi/linux/ptrace.h>

BPF_HASH(last);

int do_trace(struct pt_regs *ctx) {
    u64 ts, *tsp, delta, key = 0;

    // 读取时间戳
    tsp = last.lookup(&key);
    if (tsp != NULL) {
        delta = bpf_ktime_get_ns() - *tsp;
        if (delta < 1000000000) {
            // 如果时间小于1s，就调用bpf_trace_printk 打印
            bpf_trace_printk("%d\\n", delta / 1000000);
        }
        last.delete(&key);
    }

    // 更新时间戳ts
    ts = bpf_ktime_get_ns();
    last.update(&key, &ts);
    return 0;
}
""")

#  绑定 内核函数 ，加载BPF程序, 根据事件触发，执行钩子函数
b.attach_kprobe(event=b.get_syscall_fnname("sync"), fn_name="do_trace")
print("Tracing for quick sync's... Ctrl-C to end")


# 格式化输出
start = 0
while 1:
    try:
        (task, pid, cpu, flags, ts, ms) = b.trace_fields()
        if start == 0:
            start = ts
        ts = ts - start
        printb(b"At time %.2f s: multiple syncs detected, last %s ms ago" % (ts, ms))
    except KeyboardInterrupt:
        exit()

"""
本BPF 程序跟踪内核磁盘相关的函数 ，检测同步函数的执行时间,将同步时间小于1s的进行打印输出
    一、根据需求 确定要跟踪的 内核函数
    二、查询内核函数的请求值与返回值
    三、将BPF 函数绑定到 内核函数中，解析内核函数的返回值，使用BPF函数接收此内核函数的返回值，至于如何解析到参数


1、 bpf_ktime_get_ns 库函数，返回纳秒级时间
2、BPF_HASH(last):  bcc 宏定义创建 map ,map名为 last,但是没有指定key,value类型，默认为u64位
3、lookup() ： map 操作的之查询key ，查询map中有没有相应的key
4、 last.delete(&key);  map 删除操作
5、 last.update(&key, &ts);  map 按照key 进行更新，覆盖之前的value

"""