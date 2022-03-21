#!/usr/bin/python
#
# This is a Hello World example that formats output as fields.


from asyncio import tasks
from bcc  import  BPF
from   bcc.utils   import printb

# 1、使用C语言定义 BPF 程序，并定义成变量
prog = """
int hello(void *ctx){
    bpf_trace_printk("Hello world! \\n");
    return 0;
}
"""
# 2、 通过BPF()系统调用加载BPF程序
b = BPF(text=prog)

# 3、绑定内核事件函数,监听内核事件sys_clone,将触发执行钩子函数  hello,也就是上面定义的hello函数
b.attach_kprobe(event=b.get_syscall_fnname("clone"), fn_name="hello")

# 4、格式化打印头
print("%-18s %-16s %-6s %s" % ("TIME(s)", "COMM", "PID", "MESSAGE"))

# 5、格式化输出，监控到的数据

while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    except ValueError:
        continue
    except KeyboardInterrupt:
        exit()
    printb(b"%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))


# 本程序实现 监听内核进程Clone 事件，并格式化输出进程的 相关参数
"""
1、trace_fields 返回监听到的值，可以使用trace_print、BPF_PERF_OUTPUT()

"""    