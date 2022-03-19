# bpf_practice

`本文档记录使用bcc 工具开发ebpf程序`

## 一  、eBPF 开发环境搭建
##   二、 eBPF 程序执行流程

先来分析 eBPF开发过程 ， 如下图 （来自https://www.brendangregg.com/ebpf.html）

 ![img](https://github.com/lichenglife/bpf_practice/blob/main/hello/ebpf.jpg)  

可以将bpf程序的执行流程分成5步：

-  1、使用 C 语言开发一个 eBPF 程序； 
- 2、使用LLVM  将ebpf程序编译成BPF 字节码；
- 3、通过bpf()系统调用，将BPF字节码传递给内核；
- 4、内核对字节码进行安全校验并运行BPF程序, 将状态保存到 BPF  map 中；
- 5、用户程序通过 map 查看 内核中bpf程序运行状态；





## 三、使用bcc 开发 eBPF 程序示例

### 3.1  bcc  介绍

### 3.2  bcc  安装

bcc    安装过程参考

[官网源码安装推荐]: https://github.com/iovisor/bcc/blob/master/INSTALL.md#ubuntu---source

，但是需要注意以下两点：

- 使用较高版本的 LLVM 版本，使用11 以上
- 将python3  设为默认python 编译器 ，否则报错   BPF ImportError: No module named bcc  

### 3.3  开发hello ebpf 程序

  使用 BCC 开发 eBPF 程序，可以把前面讲到的五步简化为下面的三步。 目的开发一个ebpf程序实现在系统调用 openat()函数打开文件时，打印 Hello, World!  到 内核调试文件 /sys/kernel/debug/tracing/trace_pipe 中；依此验证通过ebpf程序可以在用户态观察到 内核态系统调用的强大功能；

- 1、使用C 开发一个 ebpf程序  hello.c

- 2、使用使用python 和BCC 库 开发 用户态程序

  ```python
  
  #!/usr/bin/env python3
  # 1) 导入了 BCC  库的 BPF 模块，以便接下来调用；
  from bcc import BPF
  
  # 2) 调用 BPF() 加载第一步开发的 BPF 源代码；
  b = BPF(src_file="hello.c")
  # 3) 将 BPF 程序挂载到内核探针
  b.attach_kprobe(event="do_sys_openat2", fn_name="hello_world")
  # 4) 读取内核调试文件 /sys/kernel/debug/tracing/trace_pipe 的内容，并打印到标准输出中。
  b.trace_print()
  ```

- 3、执行 eBPF程序，可以观察到当有 openat()系统调用发生时控制台打印 Hello,World!

  ```shell
  
  root@k8s-master:/data/bpf/bpf_practice/hello# python3   hello.py 
  b'         python3-9021    [002] d...  4607.132770: bpf_trace_printk: Hello, World!'
  b'         python3-9021    [002] d...  4607.134030: bpf_trace_printk: Hello, World!'
  b'         python3-9021    [002] d...  4607.135751: bpf_trace_printk: Hello, World!'
  b'           <...>-9161    [002] d...  7343.120474: bpf_trace_printk: Hello, World!'
  ```

   输出格式说明：

         -   python3-9021  表示进程的名称和PID
         -    [002] 表示  CPU 编号
         -   d...  表示选项
         -    4607.132770   表示时间
         -   bpf_trace_printk  表示函数
         -   Hello,World  :  入参

## 四 、eBPF中的名词解释

为了能够快速了解eBPF，以下列举一些常见的名词；