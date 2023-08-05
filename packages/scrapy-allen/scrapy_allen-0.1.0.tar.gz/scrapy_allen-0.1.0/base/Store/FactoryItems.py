from .ElasticSearch import ControlElasticSearch
from .Items import Items


class FactoryItems(object):
    @classmethod
    def create_elasticsearch_table(cls, table_name, cols_type, shards=0, replicas=0):
        type_dict = {
            "str": "keyword",
            "int": "integer",
            "float": "float",
            "text": "text",
            "bool": "bool"
        }
        if ControlElasticSearch.existsOrNot_index(table_name):
            return "index_exist"
        else:
            es_cols_type = {}
            for col in cols_type:
                # 数据类型 从标准items --> es
                es_cols_type[col] = type_dict[cols_type[col]]
            return ControlElasticSearch.creat_index(table_name, es_cols_type, shards=shards, replicas=replicas)

    @classmethod
    def createTable(cls, items:Items, **kwargs):
        if isinstance(items, Items):
            if items.store_db == "es":
                # kwargs 可选参数  shards  replicas  格式{"shards":1,"replicas":2}
                cls.create_elasticsearch_table(table_name=items.table_name, cols_type=items.cols_type,
                                               shards=kwargs.get("shards",0), replicas=kwargs.get("replicas",0))
        else:
            # list(dict(item = item).keys())[0] 获取变量的名称
            raise Exception("传入的参数%s 类型为%s 不是 Items 的子类，传入的实例需要继承Items"
                            % (list(dict(item=items).keys())[0], type(items)))
