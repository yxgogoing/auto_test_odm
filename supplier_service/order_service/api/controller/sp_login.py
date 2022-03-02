from common.objects import BaseObj
from supplier_service.order_service.api import *

class spLogin(BaseManagerService):
    def __init__(self,**kwargs):
        super(spLogin, self).__init__()
        self.info = '登录sp，返回sid给工厂端调用'
        self.uri = '/v1/auth/login'
        self.method = 'post'
        self.body = self.Body(**kwargs)
        self.resp = self.Resp

    class Body(BaseObj):
        def __init__(self,**kwargs):
            self.mobile = None  # 登录手机号
            self.password = None  # 登录密码
            BaseObj.__init__(self, **kwargs)

    class Resp(object):
        def __init__(self):
            super(spLogin.Resp, self).__init__()
            self.code = None  # None
            self.sid = self.Token()  # Noned
            self.message = None  # None

        class Token():
            def __init__(self):
                self.tokenHead = None
                self.token = None

