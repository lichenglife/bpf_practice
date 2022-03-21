from  bcc    import  BPF
# 加载 BPF  程序

b =  BPF(src_file="open.c")
# 将BPF程序绑定到内核函数
b.attach_kprobe(event = "do_sys_openat2",fname="hello_world")

print("%-18s %-16s %-6s %-16s" % ("TIME(s)", "COMM", "PID", "FILE"))

#  定义处理函数
start = 0
def  print_event(cpu,data,size):
    global start
    event =  b["events"].event(data)
    if start == 0:
             start = event.ts
    # 时间  纳秒级别         
    time_s = (float(event.ts -start)) / 1000000000
    # 打印时间、命令内容、进程PID、打开的文件名
    print("%-18.9f %-16s %-6d %-16s" % (time_s, event.comm, event.pid, event.fname))

#  将收集的事件信息
b["events"].open_perf_buffer(print_event)
while 1:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit    
