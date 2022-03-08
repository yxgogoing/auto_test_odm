# auto_test_odm

框架结构：
common
-- log  # 日志封装
-- db   # 数据库封装
-- func.py  # 测试用例中用到的方法，比如生成身份证、手机号、随机数等（根据项目添加）
-- ObjAssert.py  # 对象对比
-- objects.py  # 公共对象
-- RequestUtil.py  # request请求封装，send_requirement：把对象的入参转成json格式，拿到返回结果转成对象
-- TestHome.py  # 用例执行过程封装（装饰器套装饰器），放到对象中，后边执行只有用这个装饰器就行
-- SortUtil.py  # 排序
conf  # 配置项
-- api_host.ini  # host配置文件，可以配置业务域的host（微服务也适用）、mock、测试环境、预发环境
-- conf.py  # 操作配置文件，用的configparser库
-- db   # 数据库配置项
xxx_service
-- api
  -- controller  # 可不用（框架自动拉取swagger用例形成的接口结构，暂时没做自动拉取，看以后需要）
  -- service  # 接口结构，接口默认字段
  -- __init__  # 主要用来鉴权，避免重复鉴权
-- check
  -- BussinessInfo # 生成业务属性并可以生成期望的表结构或者返回特殊结构的期望结果
  -- ExpectObj  # 期望的对象结果，用于检测接口结构和字段是否符合预期，主要用于回归的时候检查开发是否私自改接口
  -- OrderPWutil # 查询数据库数据并返回结果,可能要结合peewee库用，暂时用不到
-- data
  -- business.py  # 存放业务状态数据，接口校验可能会作为校验项，做串流模式时用的多
  -- dynamic  # 存放动态数据，比如po单
  -- status  # 接口业务状态码，区分于请求状态，比如服务异常，po不存在，po类型错误等
-- db # 一些sql
  -- order_query_sql等


