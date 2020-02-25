import os
import time
import multiprocessing
def run_proc(name): # 子进程要执行的代码
    print ('运行子进程 %s ，子进程号为(%s)...' % (name, os.getpid()))
    print ("我的处理内容是：%s+%s=?" % (name,name))
    return name

if __name__=='__main__':
    start = time.time()
    print ('父进程号为 %s.' % os.getpid())
    print('----------------------------------------')
    job = []
    for i in range(3):
        p = multiprocessing.Process(target=run_proc, args=(i,))#多进程
        job.append(p)
        print ('子进程%d开启...'%i)
        p.start() #
        print ('子进程%d结束...'    %i)
        print
   #加join()可以让主线程一直等待全部的子线程结束之后，主线程自身才结束，程序退出
    for t in job:
        t.join()#join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步
    end = time.time()
    print (end-start)