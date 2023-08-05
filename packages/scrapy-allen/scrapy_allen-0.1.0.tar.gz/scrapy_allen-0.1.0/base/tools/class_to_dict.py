import json


class SimpleClassToDict(object):
    # 其他类继承于此类实现类转为字典类型
    def get_dict(self):
        # callable() 函数用于检查一个对象是否是可调用的。如果返回 True  简单理解，是否为函数或者方法
        # getattr() 函数用于返回一个对象属性值 例如 simpleclass_to_dict 类的属性值为 get_dict
        attrs = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        dict_val = {attr: self.__getattribute__(attr) for attr in attrs}
        return dict_val


    # 转换一个类为 字典格式 ，需传入一个类的实例
    @classmethod
    def to_dict(cls, class_):
        # class 或者 复杂dict类型 转换为 基础类型dict数据
        try:
            # 存储最终结果
            dict_result = {}
            # 如果是字典类型,则转换包含复杂数据类型dict为基础类型dict
            if type(class_) == dict:
                for elem_of_key in class_:
                    elem_of_val = class_[elem_of_key]
                    type_elem_val = type(elem_of_val)
                    if (
                            type_elem_val == bool or type_elem_val == int or type_elem_val == float or type_elem_val == str or (
                            type_elem_val is None)):
                        dict_result[elem_of_key] = elem_of_val
                    elif type_elem_val == type:
                        dict_result[elem_of_key] = str(elem_of_val)
                    else:
                        dict_result[elem_of_key] = cls.to_dict(elem_of_val)
            # 如果是类实例,则转换类实例为基础类型dict
            else:
                # 获取类实例的变量名称
                attrs = [attr for attr in dir(class_) if
                         not callable(getattr(class_, attr)) and not attr.startswith("__")]
                # 遍历变量
                for attr in attrs:
                    # 获取类实例的变量值
                    value = class_.__getattribute__(attr)
                    type_val = type(value)
                    # 如果变量值是基础类型则直接赋值
                    if type_val == bool or type_val == int or type_val == float or type_val == str or (value is None):
                        dict_result[attr] = value
                    # 如果变量本身就是类，则直接返回类名
                    elif type_val == type:
                        dict_result[attr] = str(value)
                    # 如果是list ，对list每个元素进行递归直到分解到基础类型
                    elif type_val == list:
                        list_val = []
                        for elem_of_list in value:
                            type_elem_val = type(elem_of_list)
                            if type_elem_val == bool or type_elem_val == int or type_elem_val == float or type_elem_val == str or (
                                    type_elem_val is None):
                                list_val.append(elem_of_list)
                            else:
                                list_val.append(cls.to_dict(elem_of_list))
                        dict_result[attr] = list_val
                    # 如果上述都不是，判断为class ，对class每个变量进行递归直到基础类型
                    else:
                        val_class = cls.to_dict(value)
                        dict_result[attr] = val_class
        except Exception as e:
            print("您的输入可能不合法，请输入dict字典类型或者类实例")
            dict_result = {}
        return dict_result



    @classmethod
    def to_json(cls, class_):
        dict_class = cls.to_dict(class_)
        json_class = json.dumps(dict_class)
        return json_class
