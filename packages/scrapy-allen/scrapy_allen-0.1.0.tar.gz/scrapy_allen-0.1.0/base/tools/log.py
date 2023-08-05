import logging
import os

# USEAGE
# from base.tools.log import Control_log
# log = Control_log()
# log_text = log.get_log()
#
# log_text.info("...")
# log_text.error("...")


from .config_trans_dic import TransConfigDic


class ControlLog(object):

    def __init__(self,path='',file_name="",level="info"):
        # 设置保存路径
            # 获取配置文件
        config_dic = TransConfigDic.get_config_dic()
        project_name = config_dic["project.name"]
        log_path = config_dic["log.path"]

        default_path = log_path + project_name + "/"
        path = default_path if path == '' else path
        # 如果路径不存在则创建
        if not os.path.exists(path) : os.makedirs(path)
        # 如果日志文件不存在，则根据项目文件名创建
        if file_name=="":
            file_name = "project.log"

        logfile_path = path+file_name

        # 设置日志等级
        # info(default) / debug /warn error

        log_level={
            "info":logging.INFO,
            "debug":logging.DEBUG,
            "warn":logging.WARNING,
            "error":logging.ERROR,

        }

        logging.basicConfig(level=log_level[level],#控制台打印的日志级别
                        filename=logfile_path,
                        filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                        #a是追加模式，默认如果不写的话，就是追加模式
                        format=
                        '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        #日志格式
                        )
    @classmethod
    def get_log(self):
        return logging

