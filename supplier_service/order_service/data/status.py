# 接口返回状态：订单状态
class OrderStatusCode(object):
    """response状态码"""
    OK = 200
    ServiceWrong = 500  # 服务错误
    TypeWrone = 400  # 订单类型错误
    OrderNotExit = 0  # 订单不存在
