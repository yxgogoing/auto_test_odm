from supplier_service.order_service.api.controller import sp_login as TemplateController


class Sp_Login(TemplateController):
    def __init__(self, **kwargs):
        super(Sp_Login,self).__init__(**kwargs)
        self.status = 0
        self.update_default_body()

    def update_default_body(self):
        self.mobile = None  # 登录手机号
        self.password = None  # 登录密码


    def check(self):
        pass

