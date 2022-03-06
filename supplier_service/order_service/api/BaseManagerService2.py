from common.RequestUtil import RequestUtil
from conf.conf import get_host


class BaseManagerService2(RequestUtil):
    def __init__(self):
        """域服务对象"""
        super(BaseManagerService2, self).__init__()
        self.host = get_host('odm_host')

    # def set_token(self):
    #     from supplier_service.order_service import auth_token
    #