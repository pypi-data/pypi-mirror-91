# 线程
# 是否虚拟IP
# 是否变量与爬取的值绑定
# 多个变量构成list
# 爬取过程 1. 虚拟IP header get parms
# page
# 存储位置
from base.Queue_Multi_thread.Muti_thread import Muti_thread


class Spider(object):

    def __init__(self):
        self.muti_thread = None

    def muti_thread(self, datalist, thread_num,func=None):
        """
        启动多线程# datalist : 传入外部的数据，放入队列中 []
        # thread_num : 启动线程数量
        # func : 传入的函数 限制有两个参数： 第一个参数对应线程名称， 第二个参数对应 函数传入的参数，多个参数用list 自行处理
        :param datalist: 传入外部的数据，放入队列中 []
        :param thread_num: 启动线程数量
        :param func: 传入的函数 限制有两个参数： 第一个参数对应线程名称， 第二个参数对应 函数传入的参数，多个参数用list 自行处理
        :return: 多线程实例
        """

        if func is None:
            self.muti_thread = Muti_thread(data_list=datalist, thread_num=thread_num, func=self.muti_thread_func)
        else:
            self.muti_thread = Muti_thread(data_list=datalist, thread_num=thread_num, func=func)

    def single_thread_func(self):
        """
        用户自定义爬虫方法，需要子类继承后重写方法
        :return:
        """
        pass

    def muti_thread_func(self,thread_name, data):
        """
        用户自定义爬虫方法,用于多线程使用，需要子类继承后重写方法
        :param thread_name: 线程名称，通过 muti_thread 传入
        :param data: 传入的数据通过 queue传入
        :return:
        """
        pass

    def run(self,thread_plan="single"):
        """
        执行爬虫
        :param thread_plan: single 单线程(默认)   muti 多线程 需要定义muti_thread_func 并调用 muti_thread
        :return:
        """
        if thread_plan == "single":
            self.single_thread_func()
        elif thread_plan == "muti":
            self.muti_thread.run()
        else:
            raise Exception("thread_plan 设置错误，请选择 single 单线程 or muti 多线程，不支持其他选项")
