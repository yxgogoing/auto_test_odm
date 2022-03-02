import copy, socket
import csv
import datetime
import time
import calendar
import decimal
import json
import random
import re
import hashlib
import operator
from tabulate import tabulate
from common.objects import BaseObj
from common.log.Logger import log


def merge_objs(*objs, ex=[], suffix=None):
    """
    合并对象
    :param objs:
    :param ex: 排除掉的字段
    :param suffix: 如果有重复字段则加这个作为后缀
    :return:
    """
    r = BaseObj()
    for obj in objs:
        for k, v in vars(obj).items():
            if not hasattr(r, k):
                setattr(r, k, v)
            elif k in ex:
                continue
            elif suffix:
                setattr(r, k + str(suffix), v)
    return r


# def json_to_obj(str):
#     o = BaseObj()
#     if isinstance(str, dict):
#         for k, v in str.items():
#             setattr(o, k, v)
#         return o
#     else:
#         return None


def random_str(title='公共自动化商品'):
    return title + str(random.randint(0, 100000))


def random_only():
    return random.randint(0, 1)


def random_amount():
    return round(random.random(), 2)


def random_from_list(items):
    index = random.randint(0, len(items))
    return items[index]


def random_boolen():
    return random.choice([True, False])


def random_float(n=2):
    return round(random.uniform(0, 10), n)


def random_int(start=0, end=99):
    return random.randint(start, end)


def increase_str_time():
    return datetime.datetime.now().strftime("%m%d%H%M%S%f")  # 生成当前的时间


def str_convert_to_camel(one_string, space_character):
    # one_string:输入的字符串；space_character:字符串的间隔符，以其做为分隔标志
    string_list = str(one_string).split(space_character)  # 将字符串转化为list
    first = string_list[0].lower()
    others = string_list[1:]

    others_capital = [word.capitalize() for word in others]  # str.capitalize():将字符串的首字母转化为大写

    others_capital[0:0] = [first]

    hump_string = ''.join(others_capital)  # 将list组合成为字符串，中间无连接符。
    return hump_string


def show_obj_as_excel(name, objs, ex=[]):
    headers = []
    table = []
    start_header = True
    for obj in objs:
        line = []
        for k, v in obj.__dict__.items():
            if start_header and k not in ex:
                headers.append(k)
            if k not in ex:
                line.append(v)
        table.append(line)
        start_header = False
    print('********{}********'.format(name))
    print(tabulate(table, headers=headers, tablefmt='grid'))


# 取消注释可测试show_obj_like_excel()上面的方法
# class Test():
#     def __init__(self):
#         self.name = 'yinyuting'
#         self.age = '20'
#         self.alisa = 'claire'
#
# if __name__ == "__main__":
#     objs = [Test(), Test()]
#     show_obj_like_excel('TEST', objs)

def pop_none_obj_from_list(objs):
    for index, obj in enumerate(objs):
        o = yield obj
        if is_obj_none(o):
            objs.pop(index)
    return objs


def is_obj_none(obj):
    """
    判断传入对象是否为空，为空则返回True
    """
    base = True
    if isinstance(obj, (int, str, float, decimal.Decimal)) is True:
        base &= False
    elif obj is None:
        base &= True
    else:
        for k, v in vars(obj).items():
            if v is not None:
                if isinstance(v, list):
                    if len(v) > 0:
                        for i in v:
                            base &= is_obj_none(i)
                    else:
                        base &= True
                elif is_custom_object(v):
                    base &= is_obj_none(v)
                else:
                    base &= False
            else:
                base &= True
    return base


def query_objs_attribute(objs, **kwargs):
    result = []
    for obj in objs:
        r = True
        for k, v in kwargs.items():
            try:
                e_v = getattr(obj, k)
            except Exception as e:
                check_equal(True, False, '筛选期望结果中的{0}条件{1}不正确'.format(obj, k))
            # check_equal(k not in list(obj.__dict__.keys()), False, '筛选期望结果中的{0}条件{1}不正确'.format(obj, k))
            if e_v != v:
                r = False
        if r:
            result.append(obj)
    return result


def check_equal(act_v, exp_v, err_msg=None, only_log_error=False, show_err=False):
    """
        check actual result does match expected or not
        :param string/list act_v
        :param string/list exp_v
        :param string err_msg
        :param boolean only_log_error
    """

    if err_msg is None:
        err_msg = "断言期望结果:{expectedVal}=实际结果{actualVal}".format(actualVal=act_v, expectedVal=exp_v)
    elif show_err is True:
        err_msg += ", 期望结果: {expectedVal},实际结果: {actualVal}".format(actualVal=act_v,
                                                                    expectedVal=exp_v)

    if act_v != exp_v:
        log.error(err_msg)
        if only_log_error:
            return False
        else:
            raise AssertionError(err_msg + " 失败")
    else:
        log.check(err_msg + " 成功")
    return True


def now(days=0, minutes=0, seconds=0, format="%Y-%m-%d %H:%M:%S"):
    """
    当前时间,请求时使用该格式(无时区)
    前几天后几天传delay8,or,-8
    :return:
    """
    now = datetime.datetime.now()
    d = now + datetime.timedelta(days=days, minutes=minutes, seconds=seconds)
    return d.strftime(format=format)


def time_stamp():
    return int(time.time())


def fill_in_obj_from_obj(origin_obj, from_obj, ex=[], map={}, is_convert_caps=True):
    """
    key先全部转换成小写在定位属性
    :param origin_obj: 期望的obj
    :param from_obj: 数据来源的obj
    :param ex: 排除字段
    :param is_convert_caps: 是否转换大小写
    :return:
    """
    for key, value in from_obj.__dict__.items():
        if key in ex: continue
        if key in map.keys():
            key = map.get(key)
        if is_convert_caps:
            lower_key = key.lower().replace('_', '')
            for origin_key in origin_obj.__dict__.keys():
                origin_lower_key = origin_key.lower().replace('_', '')
                if lower_key == origin_lower_key:
                    setattr(origin_obj, origin_key, value)
                    break
        else:
            for origin_key in dir(origin_obj):
                if not origin_key.startswith("__"):
                    if key == origin_key:
                        setattr(origin_obj, origin_key, value)
                        break
    return origin_obj


def to_decimal(amount, rounding='up', precision='.00'):
    """
    变更数值类型为统一2位小数的decimal格式
    :param amount:
    :return:
    """
    if amount is not None:
        if isinstance(amount, decimal.Decimal) is False:
            decimal.getcontext().prec = 10
            if rounding == 'up':
                rounding = decimal.ROUND_HALF_UP
            elif rounding == 'down':
                rounding = decimal.ROUND_DOWN
            elif rounding == 'big_up':
                rounding = decimal.ROUND_UP
            amount_decimal = decimal.Decimal(decimal.Decimal(str(amount)).quantize(decimal.Decimal(precision),
                                                                                   rounding=rounding))
            return amount_decimal
        else:
            return to_decimal(float(amount), rounding=rounding, precision=precision)
    else:
        log.info("传入amount为空，不做转换")
        return 0


def default_value(obj, key, exclude=[], default=None):
    if getattr(obj, key, None) not in exclude:
        pass
    else:
        setattr(obj, key, default)


def dict_pops(dict, keys):
    '''
    删除指定dict中的keys
    '''
    for k in keys:
        if k in dict:
            dict.pop(k)


def convert_camel_to_underline(name):
    '''
    将驼峰类型的名称转换为下划线类型的名称，如连续两个大写字母，则第二个大写自动小写，不加下划线，
    UserID == > user_id
    :param name: 驼峰类型的名称
    :return: 下划线类型的名称
    '''
    upper = []
    name = str(name)
    name = name[0].lower() + name[1:]
    for i in range(len(name)):
        if i > 0 and name[i].isupper() and name[i - 1].isupper():
            name = name[:i] + name[i].lower() + name[i + 1:]
        elif name[i].isupper():
            upper.append(i + len(upper))
    for j in upper:
        name = name[:j] + "_" + name[j].lower() + name[j + 1:]
    print(name)
    return name


def obj_convert_json(obj):
    """
    对象转化方法，转成dict或者list
    :param obj: 待转对象
    """
    try:
        from enum import Enum
        if isinstance(obj, list):
            # 如返回对象是list
            l = []
            for obj_item in obj:
                if isinstance(obj_item, (int, str, decimal.Decimal, float)):
                    l.append(obj_item)
                else:
                    l.append(obj_convert_json(obj_item))
            return l
        else:
            data = copy.deepcopy(obj.__dict__)
            for k, v in list(data.items()):
                if isinstance(v, (list, tuple)):
                    # 如对象值为list或元组
                    for index, i in enumerate(v):
                        if is_custom_object(i):
                            # 下面这句是我加的，替换掉了再下面那一坨，如果报错，请联系我  -- by cr
                            value = obj_convert_json(i)
                            # v[index] = i.__dict__

                            # value = i.__dict__
                            # for sub_k, sub_v in value.items():
                            #     if self.is_custom_object(sub_v):
                            #         value[sub_k] = self.obj_convert_json(sub_v)
                            #     elif isinstance(sub_v, (list, tuple)):
                            #         for index2, i2 in enumerate(sub_v):
                            #             if self.is_custom_object(i2):
                            #                 sub_v[index2] = i2.__dict__

                            # value = i.__dict__
                            v[index] = value
                elif isinstance(v, (Enum)):  # 枚举类，则取值
                    data[k] = v.value
                elif is_custom_object(v):
                    data[k] = obj_convert_json(v)
                elif isinstance(v, decimal.Decimal):
                    data[k] = float(v)
                elif k.startswith("_"):
                    data.pop(k)
            return data
    except Exception as e:
        log.error("请求参数对象转换成json格式出错!!!!")
        assert False

def is_custom_object(value):
    """判断是否为对象"""
    r = True

    try:
        value.__dict__
    except AttributeError as e:
        # print e
        r = False
    finally:
        return r


def delete_none_data(obj):
    """删除对象中的为None的数据"""
    obj = copy.deepcopy(obj)
    if obj is not None:
        if is_obj_none(obj) is True:
            obj = None
        else:
            for name in vars(obj):
                value = getattr(obj, name)
                if isinstance(value, list):
                    new_list = list()
                    for item in value:
                        if isinstance(item, (int, str, float)) is True:
                            new_list = value
                            break
                        new_item = delete_none_data(item)
                        # setattr(obj, name, new_item)
                        if new_item is None:
                            continue
                            # setattr(obj, name, [])
                        else:
                            new_list.append(new_item)
                    setattr(obj, name, new_list)
                elif is_custom_object(value):
                    if is_obj_none(value) is True:
                        setattr(obj, name, None)
    return obj


def get_computer_name():
    hostname = socket.gethostname()
    return hostname


def get_ip():
    ip = socket.gethostbyname(get_computer_name())
    return ip


def reader_csv():
    with open('data.csv', mode='w') as csvFile:
        reader = csv.reader(csvFile)
        for item in reader:
            print(item)


def write_csv(data, file_name='csvFile.csv'):
    if isinstance(data, dict):
        data = json.dumps(data)
    csvFile = open(file_name, 'a+')
    writer = csv.writer(csvFile)
    writer.writerow(data)
    csvFile.close()


def write_file(data, file_name='test.txt'):
    if isinstance(data, dict):
        data = json.dumps(data)
    with open(file_name, 'a+') as f:
        f.write(data)


def now_zone():
    """
    当前时间,返回时时使用该格式(带时区)
    :return:
    """
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%dT%H:%M:%S+0800")


def get_attr_value(o, attr, default):
    value = getattr(o, attr, default)
    if value is None:
        return default
    else:
        return value


def str_time_format(str_time, src_format="%Y-%m-%d %H:%M:%S", target_format="%Y-%m-%d", **kwargs):
    try:
        datetime_time = datetime.datetime.strptime(str_time, src_format) + datetime.timedelta(**kwargs)
        return datetime_time.strftime(target_format)
    except:
        return str_time


def get_month_day(year=None, month=None, format="%Y%m%d"):
    year = int(year) if year else datetime.date.today().year
    month = int(month) if month else datetime.date.today().month
    month_range = calendar.monthrange(year, month)[1]
    first_day = datetime.date(year=year, month=month, day=1).strftime(format=format)
    last_day = datetime.date(year=year, month=month, day=month_range).strftime(format=format)
    return dict(first_day=first_day, last_day=last_day)


def merge_dict_in_list(self, sql_list, *args):
    #  合并list中的字典信息
    result = []
    n = len(sql_list)
    for index in range(n):
        to_dict = {}
        for l in args:
            to_dict = self.merge_dicts(sql_list[index], l[index])
        result.append(to_dict)
    return result


def merge_dicts(one, two):
    for k in list(two.keys()):
        if k in one:
            new_k = str(k) + "2"
            one[new_k] = two[k]
        else:
            one[k] = two[k]
    return one


def attr_rename(obj, old_name, new_name, is_delete=False):
    """
    属性重命名
    :param obj: 对象
    :param old_name: 旧的属性名称
    :param new_name: 新的属性名称
    :param is_delete: 是否删除旧的属性
    :return:
    """
    if hasattr(obj, old_name):
        setattr(obj, new_name, getattr(obj, old_name))
        if is_delete:
            delattr(obj, old_name)
        else:
            pass
    else:
        return False


def batch_attr_rename(self, obj_list, old_name_list, new_name_list):
    """
    批量属性重命名
    :param obj_list:对象，最好是list
    :param old_name_list: 旧名称列表
    :param new_name_list: 新名称列表，与旧名称位置对应
    :return: None
    """
    obj_list_c = copy.deepcopy(obj_list)
    for obj in obj_list_c:
        for index, old_name in enumerate(old_name_list):
            self.attr_rename(obj, old_name, new_name_list[index])
        setattr(obj, 'carried_forward_amount', None)
    return obj_list_c


def attr_move(obj, target_name, newobj, new_name=None, is_delete=False):
    """
    移动属性到另外一个对象
    :param obj: 对象
    :param old_name: 旧的属性名称
    :param new_name: 新的属性名称
    :param is_delete: 是否删除旧的属性
    :return:
    """
    if hasattr(obj, target_name):
        if new_name:
            setattr(newobj, new_name, getattr(obj, target_name))
        else:
            setattr(newobj, target_name, getattr(obj, target_name))

        if is_delete:
            delattr(obj, target_name)
        else:
            pass
    else:
        return False


def md5_string(source_str):
    log.info(source_str)
    if not isinstance(source_str, str):
        source_str = repr(source_str)
    target = hashlib.md5()
    target.update(source_str.encode())
    targ = target.hexdigest()
    log.info(targ)

    return targ


def assert_dict_in_another_dict(small, big):
    """
    验证小dict的key和value在大dict中
    """
    small_dict = small.copy()
    big_dict = big.copy()
    diff_list = []
    for k, v in list(dict(small_dict).items()):
        print(("=======compare key as: %s" % k))
        # 浮点数抽取出，单独比较
        if isinstance(v, float) or isinstance(v, decimal.Decimal):
            decimal.getcontext().prec = 4
            small_v = decimal.Decimal(str(v))
            big_v = decimal.Decimal(str(big_dict.get(k)))
            # com.checkEqual(smallV, bigV, "check key: %s, value in big dict is: %s, value in small dict is: %s"
            #                % (k, bigV, smallV))
            if small_v != big_v:
                diff_list.append("check key: %s, value in big dict is: %s, value in small dict is: %s"
                                 % (k, big_v, small_v))
            small_dict.pop(k)
            big_dict.pop(k)
        # 比较空的情况，db和返回值里有时候是None，有时候是空字符串，拉出来单独比较
        elif v is None or v == "":
            check_equal(big_dict.get(k) is None or big_dict.get(k) == "" or big_dict.get(k) == 0, True,
                            "value not equaled, key: %s" % k)
            small_dict.pop(k)
            big_dict.pop(k)
        else:
            check_equal(str(big_dict.get(k)), str(v),
                            "check key: %s, value in big dict is: %s, value in small dict is: %s"
                            % (k, big_dict.get(k), v))
            if str(big_dict.get(k)) != str(v):
                diff_list.append("check key: %s, value in big dict is: %s, value in small dict is: %s"
                                 % (k, big_dict.get(k), v))
    if len(diff_list) > 0:
        log.error(diff_list)
        raise AssertionError(diff_list)


def get_list_elements(l):
    """
    转化int列表为字符串列表
    :param int_list: 数字列表
    :return 字符串列表
    :exp   [1,2,3]==>"1,2,3"
    """
    return str(l)[1:-1]


def convert_str_to_list(int_string):
    """
    转化字符串为数字列表
    :param int_string: 数字列表
    :return 字符串列表
    :exp   "1,2,3"==>[1,2,3]
    """
    if len(int_string) > 0:
        return list(map(int, int_string.split(",")))
    else:
        return []


def transfer_dict(raw_dict, key_convert=dict()):
    """
    用于替换字典中key名称，mapping字典中能找到即替换
    :param dict raw_dict:被转换的字典
    :param dict or None mapping:{"raw_name":"new_name"}
    :rtype: dict
    """
    global_rules = {}
    new_dict = {}
    for key in raw_dict:
        if key_convert and key in key_convert and isinstance(key_convert[key], str):  # 该字段在重命名字典中
            new_dict.update({key_convert[key]: raw_dict[key]})
        elif key_convert and key in key_convert and isinstance(key_convert[key], dict):
            new_dict.update({list(key_convert[key].keys())[0]: dict_list_rename(raw_dict[key],
                                                                                key_convert[key][
                                                                                    list(key_convert[key].keys())[
                                                                                        0]])})
        else:
            new_dict.update({global_rules[key]: raw_dict[key]} if key in global_rules else {key: raw_dict[key]})
    return new_dict


def dict_list_rename(dict_list, key_convert=dict()):
    """遍历字典列表，替换字典中的key名称"""
    new_list = []
    if isinstance(dict_list, list):
        for raw_dict in dict_list:
            new_dict = transfer_dict(raw_dict=raw_dict, key_convert=key_convert)
            new_list.append(new_dict)
        return new_list
    else:
        new_dict = transfer_dict(raw_dict=dict_list, key_convert=key_convert)
        return new_dict


def del_attrs(obj, attr_list):
    """
    批量删除属性
    :param attr_list:属性名称列表
    :return:None
    """
    if isinstance(obj, list):
        for index in range(len(obj)):
            list(map(lambda x: delattr(obj[index], x), attr_list))
    else:
        list(map(lambda x: delattr(obj, x), attr_list))


def set_attr_value_batch(obj, attr_list, value):
    """
    批量删除属性
    :param attr_list:属性名称列表
    :return:None
    """
    if isinstance(obj, list):
        for index in range(len(obj)):
            list(map(lambda x: setattr(obj[index], x, value), attr_list))
    else:
        list(map(lambda x: setattr(obj, x, value), attr_list))


def get_attr_value_batch(obj, attr_list, miss_value=None):
    """
    批量获取属性
    :param attr_list:属性名称列表
    :param miss_value:如果不到值，则给该默认值
    :return:属性值对应列表
    """
    value_list = []
    for attr in attr_list:
        value = getattr(obj, attr, miss_value)
        value_list.append(value)
    return value_list


def get_names(condition, is_all_list=False):
    """
    用于从用例描述中找出需要赋值的字段
    :param condition str:用例描述
    :param is_all_list boolean：是否全部返回list(用于屏蔽崔大神的【长度为1则取值】的特效)
    :return:
    """
    p = re.compile('[a-zA-Z]+')
    ns = re.findall(p, condition)
    if len(ns) == 1 and is_all_list == False:
        return ns[0]
    else:
        return ns


def of_course_you_are_beautiful(msg, value, obj, is_all_list=False):
    """
    根据传入的msg中的字段名称更新body中对应字段的值
    :param msg: 传入的msg
    :param value list: 需要更新的值
    :param obj: 实例的body或者param
    :param is_all_list: 是否全部返回列表
    :return:
    """
    names = get_names(msg, is_all_list=is_all_list)
    for i in range(0, len(value)):
        setattr(obj, names[i], value[i])


def amount_share_cal(amount, num):
    """按照数量平摊金额"""
    mean_list = []
    mean = to_decimal(float(amount) / float(num))
    for i in range(num):
        mean_list.append((mean))
    mean_list[-1] = to_decimal(amount) - sum(mean_list[:-1])
    return mean_list


def share_mean_caculate(amount, divisor_list):
    """按照权重计算分摊金额"""
    percent_list = []
    divisor_total = sum(divisor_list)
    for index, value in enumerate(divisor_list):
        percent = round(value / divisor_total)
        percent_list.append(percent)
    percent_list[-1] = 1 - sum(percent_list[:-1])
    return percent_list


def get_attribute(obj, attribute, default):
    """
    给对象取值,如果没有就返回默认值
    :param obj: 对象
    :param attribute: 属性名字
    :param default: 如果没有希望返回的默认值
    :return: 对象的属性值
    """
    value = getattr(obj, attribute, default)
    if value is None:
        return default
    else:
        return value


def group_list_by_method(src_list, method=operator.eq, **kwargs):
    """
    将传入的list通过制定方法进行分组，默认为相等
    ！！！attention！！！方法需要传入方法对象，不用call
    [1, 2, 3, 1, 3, 4] ==> [[1, 1], [2], [3, 3], [4]]
    """
    merged_list = list()
    index = list()
    # for key, items in groupby(src_list, key=keys):
    #     merged = []
    #     for sub_item in items:
    #         merged.append(sub_item)
    #     merged_list.append(merged)
    #
    for i in range(0, len(src_list)):
        if i in index:
            continue
        else:
            merged = [src_list[i]]
            index.append(i)
            for j in range(i + 1, len(src_list)):
                if method(src_list[i], src_list[j], **kwargs) is True:
                    merged.append(src_list[j])
                    index.append(j)
            merged_list.append(merged)
    return merged_list


def covert_resp_to_obj(obj, resp_act):
    """
    接口返回的格式如为list，目标对象需要给最外层的list命名为root，dict无所谓
    :param obj: 目标对象
    :param resp_act: 接口返回值，外层结构为list或dict
    :return:
    """

    if isinstance(resp_act, list):
        # 如果接口返回是个list，则获取接口对象中定义的外层列表属性名，获取不到则报错
        count = len(resp_act)
        root_name = None
        for name in dir(obj):
            if isinstance(getattr(obj, name), list) and name != "error_list":
                root_name = name
        if root_name is None:
            log.error("接口返回结构设置错误！！！！返回值直接为列表，请设置一个空属性包含具体返回对象！！！！")
            assert False
        if len(resp_act) > 0:
            # 如果接口返回的list长度大于0，则遍历返回，按接口生成返回对象
            if isinstance(resp_act[0], (int, float)) is False:
                # base_obj = getattr(obj, root_name)[0]
                # getattr(obj, root_name).pop()
                # for i in range(0, count):
                #     getattr(obj, root_name).append(copy.deepcopy(base_obj))
                #     _generate_resp_obj(getattr(obj, root_name)[i], resp_act[i])
                for i in range(0, count):
                    if i > 0:
                        getattr(obj, root_name).append(copy.deepcopy(getattr(obj, root_name)[0]))
                    covert_resp_to_obj(getattr(obj, root_name)[i], resp_act[i])
            else:
                setattr(obj, root_name, resp_act)
        else:
            setattr(obj, root_name, resp_act)
            log.info("return empty list")
    elif isinstance(resp_act, dict):
        for k, v in list(dict(resp_act).items()):
            if isinstance(v, dict):
                covert_resp_to_obj(getattr(obj, k), v)
                continue
            # 条件：1.是个list，2.resp_object中k对应的每一项均为dict，3.返回list不为空
            if isinstance(v, list) and len(getattr(obj, k)) and len(v) > 0:
                # 如果是个列表，则先取出第一项作为基准，再删除，然后每次遍历的时候deepcopy一个，再赋值
                count = len(v)
                base_obj = getattr(obj, k)[0]
                if isinstance(base_obj, type) is True:
                    base_obj = copy.deepcopy(base_obj)()
                getattr(obj, k).pop()
                for i in range(0, count):
                    getattr(obj, k).append(copy.deepcopy(base_obj))
                    covert_resp_to_obj(getattr(obj, k)[i], v[i])
                continue
            if hasattr(obj, k) is True:
                pass
            else:
                log.warning("接口结构{}定义中不包含属性{}，不影响结果，但建议补一下！！！！！！".format(obj, k))
            setattr(obj, k, v)
    elif isinstance(resp_act, (int, str, bool)):
        setattr(obj, "data", resp_act)
    return obj if resp_act is not None else None


def to_dict(obj):
    try:
        return obj.__dict__
    except Exception as e:
        return obj


def obj_to_json(obj):
    """
    json.dumps函数接受参数default用于指定一个函数，
    该函数能够把自定义类型的对象转换成可序列化的基本类型
    """
    return json.dumps(obj, default=to_dict)


def to_obj(j):
    try:
        return BaseObj(**j)
    except Exception as e:
        return j


def json_to_obj(j):
    """
    json.loads函数接受参数objec_thook用于指定函数，
    该函数负责把反序列化后的基本类型对象转换成自定义类型的对象
    """
    return json.loads(json.dumps(j), object_hook=to_obj)


# if __name__ == "__main__":
#     # region  序列化
#     person = BaseObj(name='tt', age=18)
#     b = BaseObj(can_do='coding')
#     person.do = b
#     person.dos = [b]
#     a_json = obj_to_json(person)
#     print(a_json)
#     # endregion
#
#     # region 反序列化
#     person = dict(name='tt',
#                   age=18,
#                   do=dict(can_do='coding'),
#                   dos=[dict(can_do='coding')])
#     person_obj = json_to_obj(person)
#     print(person_obj)

    # endregion


def get_uuid(s):
    import hashlib
    r = hashlib.md5(s.encode('utf-8'))
    return r.hexdigest()


if __name__ == "__main__":
    # print(get_uuid("jfdoajgdo2323432 "))
    # 1b67da5a559f5494eea3a058435e9bef
    # 1b67da5a559f5494eea3a058435e9bef
    s = "coupon_detail_info"
    s_list = s.split("_")  # ['abc', 'dad']
    result = s_list[0]
    for item in s_list[1:]:
        n = item.capitalize()
        result = result + n
    print(result)






