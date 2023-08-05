from base.tools.class_to_dict import SimpleClassToDict
class Items(object):
    '''
        :param store_db: 存储数据库 es: Elasticsearch
        :param table_name: 对应表名
        :param cols_type: 字段及类型 {"name":"type",...}  type: str/int/float/text ...
    '''

    type_dict = {
        "str": str,
        "int": int,
        "float": float,
        "text": str,  # 指适用于 es
        "bool": bool
    }

    @classmethod
    def get_type_dict(cls):
        return cls.type_dict

    # 继承类需要重写此三个变量
    cols_type = {}
    table_name = ""
    store_db = ""

    def __init__(self):
        for col in self.cols_type:
            setattr(self, col, None)

    def set_value(self, col, value):
        """
        设置列名所对应的数据
        :param col: 列名 字符串
        :param value: 值
        :return:
        """
        if col not in self.cols_type.keys():
            raise Exception("列名 %s 没有定义，请先在字典 %s 中定义" % (col, str(type(self))))
        elif type(value) != self.type_dict[self.cols_type[col]]:
            raise Exception("变量名称类型不匹配：传入 %s 类型为 %s，字典定义类型为%s " % (col, str(type(value)), self.cols_type["col"]))
        else:
            setattr(self, col, value)

    def get_value(self, col):
        """
        根据列名获取数据
        :param col:
        :return:
        """
        if col not in self.cols_type.keys():
            raise Exception("列名 %s 没有定义，请先在字典 %s 中定义" % (col, str(type(self))))
        else:
            return getattr(self, col, None)

    def get_dict(self):
        """
        :return: 返回变量:值，按照字典类型
        """
        class_dict = SimpleClassToDict.to_dict(self)
        return dict((key,class_dict[key]) for key in self.cols_type.keys())