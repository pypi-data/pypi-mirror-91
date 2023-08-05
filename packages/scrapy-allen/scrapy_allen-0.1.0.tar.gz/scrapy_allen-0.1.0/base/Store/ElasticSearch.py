from elasticsearch import Elasticsearch
from elasticsearch import helpers
from base.tools.config_trans_dic import TransConfigDic
from base.tools.log import ControlLog
import pandas as pd


class ControlElasticSearch(object):
    logging = ControlLog().get_log()
    conf = TransConfigDic.get_config_dic()

    # 通过配置文件获取ES配置信息
    ip_addr = conf["ES_addr"].split(",")
    # ip = ["192.168.209.21:9200","192.168.209.22:9200","192.168.209.23:9200"]
    es = Elasticsearch(ip_addr,
                       # 节点没有响应时，进行刷新，重新连接
                       sniff_on_connection_fail=True,
                       # # 每 60 秒刷新一次
                       sniffer_timeout=60
                       )

    @classmethod
    def creat_index(cls, index_name, cols={}, shards=0, replicas=0):
        """
        :param index_name: 索引名称
        :param cols: 字段，{字段名称：字段类型...}
        :param shards: 索引主分片数
        :param replicas: 索引复制分片数
        :return: success 创建成功  exist 已存在索引  error 其他为止错误，具体见日志
        """
        if shards == 0:
            shards = int(cls.conf["ES_default_index_shards"])
        if replicas == 0:
            replicas = int(cls.conf["ES_default_replicas"])

        # 索引字段及类型
        parms = {}
        mapping_ = {'properties': parms}
        for key in cols.keys():
            parms[key] = {"type": cols[key]}

        # 索引分片
        setting = {
            "number_of_shards": shards,
            "number_of_replicas": replicas
        }

        # 索引体
        body = {"settings": setting, "mappings": mapping_}

        # 返回
        callback_ = "success"
        try:
            cls.es.indices.create(index=index_name, body=body)
        except Exception as e:
            result_error = str(e)
            if result_error.__contains__('resource_already_exists_exception'):
                callback_ = "exist"
            else:
                cls.logging.error(e)
                callback_ = "error"
        finally:
            return callback_

    @classmethod
    def existsOrNot_index(cls, index_name):
        '''
        :param index_name: 索引名称
        :return: True 存在 False 不存在
        '''
        return cls.es.indices.exists(index_name)

    @classmethod
    def delete_index(cls, index_name):
        """
        :param index_name: 索引名称
        :return: True 删除索引成功  False 删除索引失败
        """
        return cls.es.indices.delete(index=index_name)['acknowledged']

    @classmethod
    def update_index(cls, index_name, cols={}):
        '''
        说明：cols 只会新增原index没有的字段
        :param index_name: 索引名
        :param cols: 更新的字段
        :return: success 更新成功  not_exist 不存在索引名，需创建 error 失败
        '''
        callback_ = 'success'
        if cls.existsOrNot_index(index_name):
            # 索引字段及类型
            parms = {}
            mapping_ = {'properties': parms}
            for key in cols.keys():
                parms[key] = {"type": cols[key]}
            cls.es.indices.put_mapping(body=mapping_, index=index_name)
        else:
            callback_ = 'not_exist'
        return callback_

    @classmethod
    def insert_value(cls, index_name, id='', body={}):
        '''
        :param index_name: 索引名称
        :param id: 行id
        :param body: 插入内容 字典格式 {}
        :return: success 执行成功  other 执行失败，返回失败原因
        '''
        callback_ = "success"
        try:
            if id == '':
                cls.es.index(index_name, body=body)
            else:
                cls.es.index(index_name, body=body, id='')
        except Exception as e:
            callback_ = str(e)
        finally:
            return callback_

    @classmethod
    def insert_value_bulk(cls, index_name, datas):
        '''
        :param index_name:
        :param datas: 传入的数据 list,每一个elem为传入的字典格式 [{},{}...]
        :return: success 执行成功  other 执行失败，返回失败原因
        '''
        callback_ = "success"
        try:
            actions = (list(map(lambda data: {
                "_index": index_name,
                "_id": data["id"],
                "_source": data
            } if "id" in data else {
                "_index": index_name,
                "_source": data
            }, datas)))

            helpers.bulk(cls.es, actions)
        except Exception as e:
            callback_ = str(e)
        return callback_

    @classmethod
    def search_value_normal(cls, index_name, cols=[], condition={}, orders={}, from_=0, size_=0):
        """
        :param index_name: 索引名称
        :param cols: 需要获取的列 [col1,col2,col3...]
        :param condition: 查询条件 格式1: {"and":[{},{},...],"or":[{},{},...]}  格式2；"name"=="zhangsan" and ("age" between [21,23] or "id" like "13238*")
        :param orders:  排序字段  格式 {"name":"asc","age":"desc",...}  优先级，前面优先
        :param from_: 从哪一条数据开始获取 int 分页使用
        :param size_: 获取多少条数据 int 分页使用
        :return: 返回完整的结果
        """
        # 查询条件体
        body = {}

        # 选择需要提取的字段
        if cols:
            body["_source"] = cols

        # 排序字段
        order_ = {}
        if orders:
            for order in orders:
                order_[order] = {"order": orders[order]}
            body["sort"] = order_

        # 切片 取部分数据
        if not (from_ == 0 or size_ == 0):
            body['from'] = from_
            body['size'] = size_

        # 查询条件过滤
        if not condition:
            body["query"] = {
                "match_all": {}
            }
        elif type(condition) == dict:
            body["query"] = {"bool": condition}
        else:
            pass

        callback_ = cls.es.search(index=index_name, body=body)
        return callback_

    @classmethod
    def search_value_df(cls, index_name, cols=[], condition={}, orders={}, from_=0, size_=0):
        original_data = cls.search_value_normal(index_name=index_name, cols=cols, condition=condition, orders=orders,
                                                from_=from_, size_=size_)

        datas = [elem["_source"] for elem in original_data["hits"]["hits"]]
        return pd.DataFrame(datas)
