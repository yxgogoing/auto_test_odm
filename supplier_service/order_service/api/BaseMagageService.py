from common.RequestUtil import RequestUtil
from conf.conf import get_host


class BaseManagerService(RequestUtil):
    def __init__(self):
        """域服务对象"""
        super(BaseManagerService, self).__init__()
        self.host = get_host('sp_host')


    def set_token(self):
        from supplier_service.order_service import auth_token
        self.update_headers(dict(Authorization=auth_token))