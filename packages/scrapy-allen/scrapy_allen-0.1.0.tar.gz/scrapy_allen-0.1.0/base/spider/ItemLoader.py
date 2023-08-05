from ..Store.Items import Items
from bs4 import BeautifulSoup,Tag


class ItermLoader(object):
    selector_type = ""
    items=[]

    def __init__(self, item: Items, selector):
        if not isinstance(item, Items):
            # list(dict(item = item).keys())[0] 获取变量的名称
            raise Exception("传入的参数%s 类型为%s 不是 Items 的子类，传入的实例需要继承Items" % (list(dict(item=item).keys())[0], type(item)))
        if isinstance(selector, BeautifulSoup) or isinstance(selector,Tag):
            # 处理传入为BeautifulSoup的数据
            self.item = item
            self.selector = selector
            self.selector_type = "BeautifulSoup"
        elif isinstance(selector, dict):
            # 处理传入为dict的数据
            self.item = item
            self.selector = selector
            self.selector_type = "dict"
        else:
            raise Exception("传入的参数%s 类型为%s 不是 BeautifulSoup/dict 的实例，传入的实例类型为BeautifulSoup/dict" % (
                list(dict(selector=selector).keys())[0], type(selector)))

    def add_value(self, col, value):
        """
        添加一个值到指定变量
        :param col: 变量名 字符串 item 会反射生成变量
        :param value:  变量值
        :return:
        """

        self.item.set_value(col, value)

    def add_selector(self, col, rule_):
        """
        从selector中根据规则获取数据
        :param col: 变量名 字符串 item 会反射生成变量
        :param rule_: 满足 BeautifulSoup select方法的规则
        :return:
        """
        if not self.selector_type == "BeautifulSoup":
            raise Exception("add_selector 方法的调用要依靠BeautifulSoup解析，在初始化时selector类型必须为BeautifulSoup")
        value_ = str(self.selector.select(rule_)[0].string)
        value = self.item.type_dict[self.item.cols_type[col]](value_)
        self.item.set_value(col, value)

    def get_item(self):
        """
        :return: 返回item
        """
        return self.item

    def get_dict(self):
        """
        :return: 按照字典格式返回结果
        """
        return self.item.get_dict()