from supplier_service.order_service.api.service.login_api import Login
from common.log.Logger import log
import parameterized
from common.TestHome import case_model


@parameterized([
    # 失败
    (dict(amount=-1), msg="验证该接口amount=-1时报xxx错", code=10005),
    param(dict(amount=None), msg="验证该接口amount=None时报错", code=10005),
    param(dict(amount="abc"), msg="验证该接口amount=\"abc\"时报错", code=10005)
])

@case_model()
def test_login(req_data={}, msg=None, code=200):
    log.step(msg)
    api_obj = Login(status=code, **req_data)
    return api_obj