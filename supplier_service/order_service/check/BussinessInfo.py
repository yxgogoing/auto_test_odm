# -*- coding: utf-8 -*-
# @Author  : yx
# @Time    : 2022/3/7 16:47

# 生成业务属性并可以生成期望的表结构或者返回特殊结构的期望结果


class BusinessInfo(object):
    def __init__(self, order_id):
        self.order_id = order_id

    def table_name_1(self):
        return [self.order_id]

    def table_name_2(self):
        return []
