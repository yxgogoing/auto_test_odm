import requests
import urllib.request, urllib.parse, urllib.error
from common.func import *
from common.log.Logger import log


headers = {'Content-Type': 'application/json',
           'Accept': 'application/json',
           "User-Agent": "tester-pc"
           }
retry_num = 3


class RequestUtil(object):
    """
    接口基础类
    """
    def __init__(self):
        self.host = None  # 域名
        self.uri = None  # uri
        self.url = None  # url host+uri+param
        self.info = None  # 描述
        self.method = None  # 请求方式 post get
        self.body = None  # 请求参数体
        self.param = None  # get请求参数
        self.resp = None  # 返回结果
        self.is_sign = None
        self.key_token = None
        self.headers = headers
        self.return_original = False  # 是否要返回dict格式的resp  功能未加进来
        # self.status_map = dict()  # status的转换
        # self.status = 0  # 期望的status值  # todo 这个走装饰器才生效
        self.success_status = 0  # 接口成功的status值
        self.http_status = 200  # http返回码
        self.timeout = 15  # 最大超时时间
        self.mock_info = BaseObj()  # mock信息

    def send_request(self,):
        log.api(type='desc', msg=self.info)  # 记录接口的中文描述
        # region 请求参数对象转换成json格式(后续发送请求使用)
        json_body = obj_to_json(self.body) if self.body else None
        json_param = obj_to_json(self.param) if self.param else None
        # endregion
        self.url = self.compose_url(json_param=json_param)  # 更新url
        resp_act = self.base_send_request(data=json_body)  # 发送请求三次重试
        self.resp = json_to_obj(resp_act)
        return self

    def update_headers(self, add_headers={}):
        self.headers.update(add_headers)

    def compose_url(self, json_param=None):
        """拼接完成的url=host+uri+params"""
        url = self.host.rstrip('/') + '/' + self.uri.lstrip('/')
        if json_param and isinstance(json_param, dict):
            para_value = urllib.parse.urlencode(json_param) if json_param else ''
        else:
            para_value = None
        para_str = ('?' + para_value) if para_value else ''
        url += para_str
        return url

    def base_send_request(self, data=None):
        """
        发送请求并判断r.status_code == 200
        :param data: json_body
        :return:
        """
        request_id = random.randint(100000, 999999)
        log.info("Send Json request and check the http status to '%s', then return dict" % self.http_status)
        log.api(type='url', msg=self.uri)
        log.info(msg="Header: {}".format(self.headers))
        log.api(type='Request Data', msg=data, deal_key=request_id)
        # if self.headers.get("Content-Type") == "application/json":
        #     data = json.dumps(data)
        # elif self.headers.get("Content-Type") == "multipart/form-data":
        #     data = MultipartEncoder(fields=self.data)
        # else:
        #     data = encodeUrlParams(self, self.data)

        r = None
        common_condition = dict(url=self.url, headers=self.headers, timeout=self.timeout)
        if self.method == "get":
            r = requests.get(**common_condition)
        elif self.method == "post":
            r = requests.post(**common_condition, data=data, allow_redirects=False)
        elif self.method == "put":
            r = requests.put(**common_condition, data=data)
        elif self.method == "delete":
            r = requests.delete(**common_condition, data=data)

        act_http_status = r.status_code
        if self.http_status != act_http_status:
            assert False, "当前请求返回状态码{}".format(act_http_status)
        elif self.http_status == 200:
            log.api(type="Response", msg=r.text, deal_key=request_id)
            return r.json()
        else:
            return None



