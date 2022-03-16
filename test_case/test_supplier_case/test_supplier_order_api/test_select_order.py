import pytest
import allure
from parameterized import parameterized, param
from supplier_service.order_service.api.controller.select_orderdetail import selectorderdetail
from supplier_service.order_service.api.controller.take_order import Takeorder
from common.log.Logger import log
from common.TestHome import case_model


@allure.feature('接单模块')
@classmethod
class Test_jiedan():
    @allure.story('查询订单')
    @parameterized([
        param(req_data=dict(tabEnName='SUPPLIER_WAIT_TAKE'), msg="查询待接单订单", code=0),
        param(req_data=dict(tabEnName='SUPPLIER_TAKEN'), msg="查询已接单订单", code=0),
        param(req_data=dict(tabEnName='SUPPLIER_EXCEPTION'), msg="查询异常订单", code=0),
        param(req_data=dict(tabEnName='SUPPLIER_CANCELED'), msg="查询已取消订单", code=0),
        param(req_data=dict(tabEnName='SUPPLIER_ALL'), msg="查询全部订单", code=0),
        ])
    @case_model()
    def test_select_order(req_data={}, msg=None, code=200):
        log.step(msg)
        api_obj = selectorderdetail(status=code, **req_data)
        return api_obj


    @allure.story('接单')
    @parameterized([
        # 正向用例：失败
        param(req_date=dict(purchaseOrderNoList='10000,6787'), msg="验证订单号不符合规则时报错", code=0),
        param(req_data=dict(purchaseOrderNoList=None), msg="验证订单号=None时报错", code=0),
        param(req_data=dict(purchaseOrderNoList="abc"), msg="验证该接口订单号=\"abc\"时报错", code=0),
        # 正向用例：成功
        param(req_data=dict(purchaseOrderNoList='PO2022022800002,PO2022022800002'), msg="订单号是多个时接单"),
        param(req_data=dict(purchaseOrderNoList='PO2022012600014'), msg="验证订单号正常时成功")
    ])
    @case_model()
    def test_takeorder(req_data={}, msg=None, code=200):
        log.step(msg)
        api_obj = Takeorder(status=code, **req_data)
        return api_obj
