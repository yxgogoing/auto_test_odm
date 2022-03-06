from parameterized import parameterized, param
from supplier_service.order_service.api.login_service.login_api import LoginObj
from common.log.Logger import log
from common.TestHome import case_model


@parameterized([
    param(dict(amount=-1), msg="验证该接口amount=-1时报xxx错", code=10005),
    param(dict(amount=None), msg="验证该接口amount=None时报错", code=10005),
    param(dict(amount="abc"), msg="验证该接口amount=\"abc\"时报错", code=10005)
])
@case_model()
def test_login(req_data={}, msg=None, code=200):
    log.step(msg)
    api_obj = LoginObj(status=code, **req_data)
    return api_obj
