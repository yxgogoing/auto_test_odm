from common.log.Logger import log
from parameterized import parameterized, param
from common.TestHome import case_model
from supplier_service.order_service.api.controller.take_order import Takeorder
import pytest
import allure

# parameterized为第三方开源库，对源代码有做修改已支持py4.0框架以及args or kwargs两种模式
@parameterized([
    # 正向用例：失败
    param(req_date=dict(purchaseOrderNoList=10000), msg="验证订单号不符合规则时报错", code=0),
    param(req_data=dict(purchaseOrderNoList=None), msg="验证订单号=None时报错", code=0),
    param(req_data=dict(purchaseOrderNoList="abc"), msg="验证该接口订单号=\"abc\"时报错", code=0),
    # 正向用例：成功
    param(req_data=dict(purchaseOrderNoList='PO2022022800002,PO2022022800002'), msg="订单号是多个时接单"),
    param(req_data=dict(purchaseOrderNoList='PO2022012600014'), msg="验证订单号正常时成功",code=0),
])  # 第三方库参数化风格
@case_model()
def test_takeorder(req_data={}, msg=None, code=200):
    log.step(msg)
    api_obj = Takeorder(status=code, **req_data)
    return api_obj
