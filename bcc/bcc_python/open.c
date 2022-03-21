#include <uapi/linux/openat2.h>
#include <linux/sched.h>

// 定义数据结构

struct date_t
{
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    char fname[NAME_MAX];
};

// 定义性能事件映射map 
BPF_PERF_OUTPUT(events);

//  定义 内核处理函数,如何处理参数
int hello_world(struct pt_regs *ctx,int dfd,const  char __user *filename, struct open_how *how){

   struct  data_t  data =  {  };
   // 获取进程的 PID  以及时间
   data.pid = bpf_get_current_pid_tgid();
   data.ts = bpf_ktime_get_ns();

   // 获取进程名
   if (bpf_get_current_comm(&data.comm, sizeof(data.comm)) == 0)
   {
       bpf_probe_read(&data.fname,sizeof(data.fname),(void*)filename);
    }
    
    // 提交性能事件，将事件提交到  map中，用于用户态读取
    events.perf_submit(ctx, &data, sizeof(data));
    return 0;
}

/**
 *  上面的程序使用 BCC 定义的一系列的库函数和宏定义
 * PPF_PERF_OUTPUT: 定义一个 perf  事件类型的  BPF映射，需要调用perf_submmit()把数据提交到BPF映射中；
 * bpf_get_current_pid_tgid 用于获取进程的 TGID 和 PID；
 * bpf_ktime_get_ns 用于获取系统自启动以来的时间，单位是纳秒；
 * bpf_get_current_comm 用于获取进程名，并把进程名复制到预定义的缓冲区中；
 * bpf_probe_read 用于从指定指针处读取固定大小的数据，这里则用于读取进程打开的文件名。
 */