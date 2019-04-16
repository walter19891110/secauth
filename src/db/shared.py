# -*- encoding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 设置MySQL数据库
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'walter135790'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'secauth'

# mysql 不会认识utf-8,而需要直接写成utf8
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME,
                                                                       PASSWORD, HOST, PORT, DATABASE)

# 初始化数据库连接
db_engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=50, max_overflow=50, pool_timeout=60)

# 测试时可以使用sqlite3 数据库
test_db_engine = create_engine("sqlite:////usr/local/ngsp/secauth/db/test.db")  # 在当前路径创建sqlite数据库

# 创建DBSession类型
# DBSession = sessionmaker(bind=db_engine)
DBSession = sessionmaker(bind=test_db_engine)

# 创建session对象
session = DBSession()
