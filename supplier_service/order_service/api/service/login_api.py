from supplier_service.order_service.api.service import sp_login_api  as TemplateController


class Login(TemplateController):
    def __init__(self,**kwargs):
        super(Login,self).__init__(**kwargs)
        self.status = 0 # 登录成功返回0
        self.update_default_body()

    def update_default_body(self):
        self.accountId = '2028'  # 供应商主体id
        self.sid = None  # sid
        self.supplierId = '3759'  # 供应商id

    def check(self):
        pass
