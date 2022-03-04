# auto_test_odm

框架结构：
common
-- log  # 日志封装
-- db   # 数据库封装
-- func.py  # 测试用例中用到的方法，比如生成身份证、手机号、随机数等（根据项目添加）
-- ObjAssert.py  # 对象对比
-- objects.py  # 公共对象,将用例
-- RequestUtil.py  # request请求封装，send_requirement：把对象的入参转成json格式，拿到返回结果转成对象
-- TestHome.py  # 用例执行过程封装（装饰器套装饰器），放到对象中，后边执行只有用这个装饰器就行
-- SortUtil.py  # 排序
conf  # 配置项
-- api_host.ini  # host配置文件，可以配置业务域的host（微服务也适用）、mock、测试环境、预发环境
-- conf.py  # 操作配置文件，用的configparser库
-- db   # 数据库配置项
xxx_service
-- api
  -- controller  # 可不用（框架自动拉取swagger用例形成的接口结构）
  -- service  #
  -- __init__  #
-- check
  -- 
  
-- data
  -- business.py  # 存放业务数据
  -- dynamic  # 存放动态数据
  -- status  # 业务状态码


