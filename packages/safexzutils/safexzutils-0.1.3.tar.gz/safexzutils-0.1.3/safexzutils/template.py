#coding=utf-8
import sys
import os
import inspect

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from common import get_tb_info

class CTemplate(object):
    def __init__(self,ruleconf={}):
        self.m_ruleconf = ruleconf

    def hello(self):
        # print("CTemplate:hello")
        return 0

    def compute(self, *args, **kwargs):
        rule_name = kwargs.get('rule_name')
        if rule_name not in dir(self):
            msg = "类{0}的函数中没有[{1}]".format(type(self).__name__, rule_name)
            result = {"result": 1, "data": -1, "message": msg}
        elif rule_name not in self.m_ruleconf:
            msg = "配置文件rule.yaml中，没有该变量[{0}]".format(rule_name)
            result = {"result": 1, "data": -1, "message": msg}
        else:
            try:
                ## 监听函数地址
                _handler = getattr(self, rule_name)

                ## 获取监听函数参数
                _handler_params = inspect.signature(_handler).parameters

                ## 下游函数解析
                _handle_kwargs = {}
                if "kwargs" in _handler_params:
                    _handle_kwargs.update(kwargs)
                else:
                    other_params = {key: kwargs.get(key) for key in kwargs if key in _handler_params}
                    _handle_kwargs.update(other_params)

                result = _handler(*args, **_handle_kwargs)

            except:
                msg = get_tb_info()
                result = {"result": 1, "data": -1, "message": msg}
        return result


if __name__ == "__main__":
    pass
