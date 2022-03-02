# -*- coding:utf-8 -*-
# @Time : 2022/3/2 14:01
# @Author : yx
# @File : TestHome1.py

from functools import wraps


def case_model(compare_hook=None, compare_obj=None, check_id=None):
    """

    :param compare_hook:
    :param compare_obj:
    :param check_id:
    :return:
    """
    def deco_resp(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(('执行用例 %s():' % func.__name__))
            api_obj_a = func(*args, **kwargs)
            if isinstance(api_obj_a, list):
                api_objs = api_obj_a
            else:
                api_objs = [api_obj_a]
            for api_obj in api_objs:
                api_obj.send_request()
                if compare_hook and compare_obj:
                    if check_id is None:
                        compare_hook(api_obj, compare_obj)
                        # check(api_obj, compare_obj)
                    else:
                        compare_hook(api_obj, compare_obj, check_id)
                else:
                    api_obj.check()
        return wrapper
    return deco_resp

