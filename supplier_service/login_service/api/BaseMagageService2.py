from common.RequestUtil import RequestUtil
from conf.conf import get_host


class BaseManagerService2(RequestUtil):
    def __init__(self):
        """域服务对象"""
        super(BaseManagerService2, self).__init__()
        self.host = get_host('odm_host')

    def set_user(self, user=None):
        from supplier_service.login_service.api.login_service.user_info import user as default_user
        user = user if user else default_user
        self.update_headers(dict(Authorization=user))

