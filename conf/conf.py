import configparser, os

conf_path = os.path.dirname(os.path.abspath(__file__))
# conf_file = os.path.join(conf_path, "conf")
root_path = os.path.dirname(conf_path)


def get_conf(path):
    conf = configparser.ConfigParser()
    conf.read(path, encoding='utf-8')
    return conf


def host_conf():
    conf = get_conf(path=os.path.join(conf_path, "api_host.ini"))
    return conf


def db_conf():
    conf = get_conf(path=os.path.join(conf_path,
                                      "mysql.ini"))
    return conf


def get_host(host):
    section = "host"
    conf = host_conf()
    return conf.get(section, host)


