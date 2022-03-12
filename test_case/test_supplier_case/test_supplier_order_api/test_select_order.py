from parameterized import parameterized, param
from supplier_service.order_service.api.controller.select_orderdetail import selectorderdetail
from common.log.Logger import log
from common.TestHome import case_model


@parameterized([
    param(dict(tabEnName='SUPPLIER_WAIT_TAKE'), msg="查询待接单订单", code=0),
    param(dict(tabEnName='SUPPLIER_TAKEN'), msg="查询已接单订单", code=0),
    param(dict(tabEnName='SUPPLIER_EXCEPTION'), msg="查询异常订单", code=0),
    param(dict(tabEnName='SUPPLIER_CANCELED'), msg="查询已取消订单", code=0),
    param(dict(tabEnName='SUPPLIER_ALL'), msg="查询全部订单", code=0),
])
@case_model()
def test_select_order(req_data={}, msg=None, code=200):
    log.step(msg)
    api_obj = selectorderdetail(status=code, **req_data)
    return api_obj
