from supplier_service.login_service.api.controller.loginobj import LoginObj as TC

class Login(TC):
    def __init__(self,**kwargs):
        super(Login, self).__init__(**kwargs)
        self.status = 0 # 登录成功返回0
        self.update_default_body(**kwargs)

    def update_default_body(self, **kwargs):
        self.accountId = '2028'  # 供应商主体id
        self.sid = None  # sid
        self.supplierId = '3759'  # 供应商id
        self.body.update_value(**kwargs)

    def check(self):
        pass


