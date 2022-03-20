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

关于bpf程序什么时候执行，在bpf程序加载至内核后，需要与内核函数调用事件进行绑定，当内核事件（ 系统调用、内核跟踪点、内核函数和用户态函数的调用退出、网络事件 等等）触发时，则执行bpf程序；

总结下来就是 用高级语言开发的 eBPF 程序，需要首先编译为 BPF 字节码，然后借助 bpf 系统调用加载到内核中，最后再通过性能监控等接口与具体的内核事件进行绑定。这样，内核的性能监控模块才会在内核事件发生时，自动执行我们开发的 eBPF 程序。 



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

   - python3-9021  表示进程的名称和PID

   -  [002] 表示  CPU 编号

   - d...  表示选项

   -  4607.132770   表示时间

   - bpf_trace_printk  表示函数

   - Hello,World  :  入参，在bpf程序中定义的参数


​     

## 四 、bpf程序的运行原理



- 4.1 eBPF 虚拟机 原理

- 4.2  eBPF程序绑定事件原理   

     ebpf程序如何绑定到内核事件？

- 4.3  系统调用bpf() 介绍说明

  用户态程序与内核态程序交互是通过 bpf系统调用完成的

  执行  man   bpf, 查看bpf系统调用的格式

  ```shell
  int bpf(int cmd, union bpf_attr *attr, unsigned int size);
  ```

   执行 bpftool   prog  list  查看所有的系统调用

   

  参数说明：

           - 第一个参数： cmd  代表操作命令
           - 第二个参数： 代码eBPF程序类型，不同的类型传入不同的类型属性指针
           - 第三个参数： 代表属性大小

- 4.3  eBPF  指令执行

- 4.4   辅助函数

     Linux内核定义了一系列内核函数 供 eBPF程序进行调用，这些函数统称为辅助函数。eBPF程序只能调用内核提供的辅助函数，eBPF 社区的发展，也是因为Linux 内核支持更多的辅助函数，由最早的包过滤，扩展到事件跟踪、安全等模块。

  执行 bpftool feature probe 查看当前系统支持哪些辅助函数，见同级目录文件HelperCalls.sh

- 4.5   BPF  映射
- 4.6  BPF 类型格式 (BTF) 

##  五 BPF 程序类型以及事件触发机制



##  六  名词解释

学习BPF  过程中会涉及以下名词，这里先进行了解

- BPF

- eBPF

-  bpftool  工具

- BPF 操作命令

   

  | BPF 命令 | 功能描述 | 备注 |
  | -------- | -------- | ---- |
  |          |          |      |
  |          |          |      |
  |          |          |      |
  |          |          |      |
  |          |          |      |
  |          |          |      |
  |          |          |      |

  

- eBPF 程序类型 根据作用分类

- BPF 辅助函数

- 探针

  

