from common.objects import BaseObj
from supplier_service.order_service.api.BaseMagageService2 import BaseManagerService2

# from sp_login import spLogin

class Login():
    def __init__(self,**kwargs):
        super(Login, self).__init__()
        self.info = '登录后返回token'
        self.uri = '/v2/auth/login'
        self.method = 'post'

    class Body(BaseObj):
        def __init__(self, **kwargs):
            self.accountId = None  # 供应商主体id
            self.sid = None  # sid
            self.supplierId = None  # 供应商id
            BaseObj.__init__(self, **kwargs)

    class Resp(object):
        def __init__(self):
            super(Login.Resp, self).__init__()
            self.code = None  # None
            self.data = self.Token()  # None
            self.message = None  # None

        class Token(object):
            def __init__(self):
                self.tokenHead = None
                self.token = None



