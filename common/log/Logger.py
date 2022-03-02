import logging, sys, re
import json


class Logger(object):
    def __init__(self, msg=None):
        sys.stderr = sys.stdout  # 解决pycharm会将所有stderr变成红色
        self.logger = logging.getLogger()  # new一个log对象
        # coloredlogs.install(level='INFO', logger=self.logger)
        ch = logging.StreamHandler()  # 所有输入会到stderr中
        self.logger.setLevel('INFO')  # 设置info级别以上log会被显示
        # self.logger.handlers[0].level = 20
        # 设置日志格式
        # LOGFORMAT = "%(log_color)s[%(name)s]%(asctime)s: %(log_color)s%(message)s"
        LOGFORMAT = "[%(name)s]%(asctime)s: %(message)s"
        # formatter = ColoredFormatter(LOGFORMAT)
        formatter = logging.Formatter(LOGFORMAT, datefmt="[%H:%M:%S]")  # 去掉log日期，没必要展示
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.center = 11

    def info(self, msg=""):
        self.logger.name = 'INFO'
        if msg == "":
            msg = "start api test: {}".format(sys._getframe().f_back.f_code.co_name)
        self.logger.info(msg=msg)

    def _info(self, msg=""):
        if msg:
            self.logger.info(msg)

    def warning(self, msg=""):
        self.logger.name = 'WARNING'
        self.logger.warning(msg=msg)

    def error(self, msg=""):
        self.logger.name = 'ERROR'
        # print(msg)
        if msg:
            error_msg = "\033[1;35m " + str(msg) + " \033[0m!"
            self.logger.error(msg=error_msg)  # 兼容控制台打印

    def mysql(self, msg=""):
        self.logger.name = 'MYSQL'
        db_host = msg[-1]
        sql_str = self._pw_sql_format(msg[0])

        if sql_str:
            self.logger.info(msg="[{}]".format(db_host) + ":" + sql_str)

    # def formmat_error(self, title, content):
    #     """
    #     格式化显示日志
    #     """
    #     self.error(msg=self._format_str(title=title, content=content))
    #
    # def formmat_info(self, title, content):
    #     """
    #     格式化显示日志
    #     """
    #     self.info(msg=self._format_str(title=title, content=content))

    def step(self, msg=None):
        """该log仅在test case方法下出现,会更新case名称"""
        # self._info(name='STEP')
        self.logger.name = 'STEP'
        if msg:
            self.logger.info(msg)
        else:
            msg = "start api test: {}".format(sys._getframe().f_back.f_code.co_name)
            self.logger.info(msg)

    def check(self, msg):
        self.logger.name = 'CHECK'
        # print(msg)
        if msg:
            self.logger.info(msg=msg)

    def api(self, type, msg="", deal_key=None):
        """
        记录发送请求的log信息
        desc: 请求的描述
        url: 请求的url
        request_data:请求参数
        resp:返回参数
        """
        self.logger.name = 'API'
        desc = "desc"
        url = "url"
        request = "Request Data"
        response = "Response"
        if msg:
            if type == desc:
                self.logger.name = 'API_DESC'  # 请求的中文描述
            elif type == url:
                self.logger.name = 'API_URL'
            elif type == request:
                self.logger.name = 'API_REQUEST_{}'.format(deal_key)
                try:
                    msg = json.dumps(json.loads(msg), ensure_ascii=False, indent=2)
                except Exception as e:
                    self.error(e)
            elif type == response:
                self.logger.name = 'API_RESPONSE_{}'.format(deal_key)
                try:
                    msg = json.dumps(json.loads(msg), ensure_ascii=False, indent=2)
                except Exception as e:
                    self.error(e)
            else:
                error_msg = "api log类型错误:请传入\"{desc},{url},{request},{response}\"api log类型".format(desc=desc,
                                                                                                   url=url,
                                                                                                   request=request,
                                                                                                   response=response)
                self.error(error_msg)
                raise NameError(error_msg)
                # print(msg)
        # msg = msg.replace("\'","\"")
        self.logger.info(msg=msg)  # 兼容控制台打印

    # =======================私有方法================================
    def _format_str(self, title=None, content=None):
        a = format(title, "=^120")
        b = format("", "=^120")
        str_content = str(content).replace("}, {", "},\n{")
        return "\n".join(("\n", a, str_content, b))

    # def write_file(self, data, file_name=FILE_NAME):
    #     # 写入之前先检查用例是否有变动
    #     if data:
    #         if isinstance(data, dict):
    #             data = json.dumps(data,ensure_ascii=False)
    #         with open(file_name, 'a+', encoding='utf-8') as f:
    #             # path = sys.argv[1].split('/')[-1]  # 获取写入文件时候被执行的用例的路径
    #             f.write(self.logger.name + ":" + data + '\n')
    def _pw_sql_format(self, msg=""):
        """pw_sql格式化为可直接用于查询的字符串"""
        sql_str = ""
        try:
            if msg:
                for index, arg in enumerate(msg[1]):
                    # 用于为参数列表中的日期参数加入引号
                    mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", str(arg))
                    if mat:
                        msg[1][index] = "'{arg}'".format(arg=arg)
                    if arg == None:
                        msg[1][index] = "Null"

                sql_str = msg[0] % tuple(msg[1])
            # 去除搜索列名，用*代替
            if "UNION" not in sql_str:
                # sql_split_list=re.split("SELECT|FROM",sql_str)
                sql_split_list = sql_str.split("FROM")
                sql_split_list[0] = 'SELECT `t1`.`*`'
                sql_str = "FROM".join(sql_split_list)
        except:
            pass
        return sql_str


log = Logger()
