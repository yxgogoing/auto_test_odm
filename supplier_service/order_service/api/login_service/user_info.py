from common.RequestUtil import RequestUtil


class UserInfo(object):
    def __init__(self, mobile, password):
        self.mobile = mobile
        self.password = password
        # self.guid = None
        # self.zuulToken = None

    def login(self):
        # 调用sp_login_api
        from supplier_service.order_service.api.login_service.sp_login_api import spLogin
        from common.RequestUtil import RequestUtil
        sp_login_api = spLogin().send_request()
        sid = sp_login_api.resp.data.sid
        print(sid)
        # 调用login_api
        from supplier_service.order_service.api.login_service.login_api import Login
        login_api = Login(sid=sid).send_request()
        self.guid = login_api.resp.data.guid
        self.zuulToken = login_api.resp.data.zuulToken


user = UserInfo(mobile='13122233333', password='33333').login()