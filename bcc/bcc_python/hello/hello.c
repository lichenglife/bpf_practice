/**
 * @file hello.c
 * @author your name (you@domain.com)
 * @brief   使用C写一个eBPF程序
 * @version 0.1
 * @date 2022-03-21
 * 
 * @copyright Copyright (c) 2022
 * 
 */

int  hello_world(void *ctx)
{
    bpf_trace_printk("Hello world!");
    return 0;
}

/**
 * 1、bpf_trace_printk 是 BPF内核函数，作用是输出字符串，在内核事件触发时，将字符串"Hello world"输出到Linux的调试文件中
 * /sys/kernel/debug/tracing/trace_pipe
 *
 */