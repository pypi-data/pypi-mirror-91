import os


class TransConfigDic(object):
    dic_config = {}
    try:
        config_path = os.path.dirname(__file__).replace("\\","/").replace("base/tools","config/project.properties")
        f = open(config_path, 'r')
        for line in f.readlines():
            line = line.replace(" ", "").replace("\t", "")
            # 如果字符头为# 表示注释 或者空行，则跳过
            if line[0] == '#' or line == '\n':
                continue
            # 处理配置文件每一行，去掉多余空格，去掉行末换行符， = 前为字典名 = 后为字典值
            if line.__contains__("="):
                line = line.strip('\n')
                configline = line.split("=")
                if len(configline) != 2:
                    raise Exception("配置文件 project.properties 有误，一行中有多个 = 号")
                dic_config[configline[0]] = configline[1]
            else:
                raise Exception("配置文件 project.properties 有误，缺少'='")
        f.close()
    except Exception as e:
        print(e)


    @classmethod
    def get_config_dic(cls):
        return cls.dic_config
