from common.objects import BaseObj
from supplier_service.login_service.api.BaseMagageService2 import BaseManagerService2

class selectorderdetail(BaseManagerService2):
    def __init__(self,status=200,**kwargs):
        super(selectorderdetail, self).__init__()
        self.info = '查询订单'
        self.uri = 'v1/purchase-order/querySupplierOrderPage'
        self.method = 'post'
        self.body = self.Body(**kwargs)
        self.resp = self.Resp
        self.status = status
        self.set_user()



    class Body(BaseObj):
        def __init__(self, **kwargs):
            self.page = 1 # 查询第一页
            self.pageSize = 50  # 默认查询50条数据
            self.tabEnName = None  # 查询的订单状态
            BaseObj.__init__(self, **kwargs)

    class Resp(object):
        def __init__(self):
            super(selectorderdetail.Resp, self).__init__()
            self.code = None  # None
            self.data = None  # Noned
            self.message = None  # None

    def check(self):
        pass
