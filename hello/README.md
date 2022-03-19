# bpf_practice

`本文档记录ebpf开发流程`

## 一  、eBPF  开发环境搭建
##   二、 eBPF 程序执行流程

先来分析 eBPF开发过程 ， 如下图 （来自https://www.brendangregg.com/ebpf.html）

 ![img](https://github.com/lichenglife/bpf_practice/blob/main/hello/ebpf.jpg)  

可以将bpf程序的执行流程分成5步：

-  1、使用 C 语言开发一个 eBPF 程序； 
- 2、使用LLVM  将ebpf程序编译成BPF 字节码；
- 3、通过bpf()系统调用，将BPF字节码传递给内核；
- 4、内核对字节码进行安全校验并运行BPF程序, 将状态保存到 BPF  map 中；
- 5、用户程序通过 map 查看 bpf程序运行状态；





## 三、使用bcc 开发 ebpf 程序

### 3.1  bcc  介绍

### 3.2 bcc  安装

### 3.3  开发hello ebpf 程序

 