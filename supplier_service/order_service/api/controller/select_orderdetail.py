# -*- coding: utf-8 -*-
# @Author  : XerCis
# @Time    : 2022/3/7 16:18

from common.objects import BaseObj
from supplier_service.login_service.api.BaseMagageService2 import BaseManagerService2

class orderdetail():
    def __init__(self,**kwargs):
        super(orderdetail, self).__init__()
        self.code = None
        self.data = None


        self.body = self.Body(**kwargs)


    class Body(BaseObj):
        pass


