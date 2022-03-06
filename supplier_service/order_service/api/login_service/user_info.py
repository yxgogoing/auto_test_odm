

class UserInfo(object):
    def __init__(self, mobile, password):
        self.mobile = mobile
        self.password = password
        # self.guid = None
        # self.zuulToken = None

    def login(self):
        # 调用sp_login_api
        from supplier_service.order_service.api.login_service.sp_login_api import spLogin
        sp_login_api = spLogin(mobile=self.mobile,
                               password=self.password).send_request()
        sid = sp_login_api.resp.data.sid
        print(sid)
        # 调用login_api
        from supplier_service.order_service.api.login_service.login_api import Login
        login_api = Login(sid=sid).send_request()


user = UserInfo(mobile='13430212979', password='chaowen666').login()
