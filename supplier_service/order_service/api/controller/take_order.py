from common.objects import BaseObj
from supplier_service.login_service.api.BaseMagageService2 import BaseManagerService2

class Takeorder(BaseManagerService2):
    def __init__(self, status=200,**kwargs):
        super(Takeorder, self).__init__()
        self.info = '接单'
        self.uri = 'v1/purchase-order/takeOrder'
        self.method = 'post'
        self.body = self.Body(**kwargs)
        self.resp = self.Resp
        self.status = status
        self.set_user()


    class Body(BaseObj):
        def __init__(self,**kwargs):
            self.operatorId = None  # 操作人uid
            self.operatorName = None  # 操作人名称
            self.purchaseOrderNoList = None  # 采购单号列表
            self.supplierid = 3571  # 供应商id，不传就随机取
            BaseObj.__init__(self, **kwargs)



    class Resp(object):
        def __init__(self):
            self.code = None
            self.data = None
            self.error = None
            self.isSuccess = 1  # 业务成功标记，成功为1
            self.message = None
            self.timestamp = None

    def check(self):
        pass







