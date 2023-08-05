import queue
import threading
import time

#说明 ： 1. 创建 线程对象    2启动线程

class Muti_thread(object):
    exitFlag = 0
    data_lis=[]
    queueLock = threading.Lock()
    workQueue = queue.Queue()
    func = None
    thread_num=0
    threadID = 1


    class myThread(threading.Thread):
        def __init__(cls, threadID, name,outclass):
            #outclass 传入外部类的实例
            threading.Thread.__init__(cls)
            cls.threadID = threadID
            cls.name = name
            cls.outclass = outclass

        def run(cls):
            # print("开启线程：" + cls.name)
            cls.outclass.process_data(cls.name)  # 执行外部类的方法
            # print("退出线程：" + cls.name)

    def __init__(self,data_list, thread_num , func):
        # datalist : 传入外部的数据，放入队列中 []
        # thread_num : 启动线程数量
        # func : 传入的函数 限制有两个参数： 第一个参数对应线程名称， 第二个参数对应 函数传入的参数，多个参数用list 自行处理
        data_lis = data_list.copy()
        self.thread_num = thread_num
        self.func = func
        self.threads = []
        self.threadID = 1
        # 填充队列
        self.queueLock.acquire()
        for elem in data_lis:
            self.workQueue.put(elem)
        self.queueLock.release()

    def process_data(self,thread_name):
        # 外部传入的数据加入到队列，并执行外部函数
        while not self.exitFlag:
            self.queueLock.acquire()
            if not self.workQueue.empty():
                data = self.workQueue.get()
                num_remain = self.workQueue.qsize()
                self.queueLock.release()
                self.func(thread_name, data)
                # print("queue remain " +str(num_remain))
            else:
                self.exitFlag=1
                self.queueLock.release()

    def run(self):
        # 创建多线程，启动线程，等待结束
        threadList = map(lambda x:"thread-"+str(x),range(self.thread_num))
        # 创建新线程
        for tName in threadList:
            thread = self.myThread(self.threadID, tName,self)
            thread.start()
            self.threads.append(thread)
            self.threadID += 1

        # 等待所有线程完成
        for t in self.threads:
            t.join()
        # print("退出主线程")