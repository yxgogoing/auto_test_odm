from parameterized import parameterized, param
from supplier_service.order_service.api.controller.select_orderdetail import selectorderdetail
from common.log.Logger import log
from common.TestHome import case_model


@parameterized([
    param(dict(amount=-1), msg="验证该接口查询不存在的订单号", code=10005),
    param(dict(amount=None), msg="多个订单查询", code=10005),
    param(dict(amount="abc"), msg="验证该接口amount=\"abc\"时报错", code=10005)
])
@case_model()
def test_select_order(req_data={}, msg=None, code=200):
    log.step(msg)
    api_obj = selectorderdetail(status=code, **req_data)
    return api_obj
