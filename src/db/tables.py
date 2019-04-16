# -*- encoding:utf-8 -*-

# 定义表结构
from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from db.shared import db_engine
from db.shared import test_db_engine

# 创建对象的基类:
Base = declarative_base()


class DeviceInfo(Base):
    """设备信息表，
    devID：设备ID
    devIC：设备识别码
    userlist：可使用该设备的用户名列表
    """
    # 定义表名
    __tablename__ = 'device_info'
    # 定义列对象
    devID = Column(String(256), primary_key=True)  # 设备ID，主机名
    devIC = Column(String(256))  # 设备唯一识别码
    userlist = Column(Text)  # 可使用该设备的用户名列表，用户名之间用逗号隔开


class User(Base):
    """用户基本信息表
    username：用户名，全网唯一
    password：用户密码
    userrole：用户角色，多个角色逗号隔开
    range：使用范围：0 全网账号 1本地账号
    realname：真实姓名
    groupID：所在用户组
    orgID：所在调度机构
    phone：手机号
    """
    # 定义表名
    __tablename__ = 'users'
    # 定义列对象
    username = Column(String(256), primary_key=True)
    password = Column(String(256))
    userrole = Column(String(256))
    range = Column(Integer)
    realname = Column(String(256))
    groupID = Column(String(256))
    orgID = Column(String(256))
    phone = Column(String(256))


class UserLogin(Base):
    """用户登录信息表
    username：用户名
    loginstatus：登录状态，0 登录 1 退出
    logintime：登录时间
    loginhost：登录终端名
    """
    # 定义表名
    __tablename__ = 'user_login'
    # 定义列对象
    username = Column(String(256), primary_key=True)
    loginstatus = Column(Integer)
    logintime = Column(String(256))
    loginhost = Column(String(256))


class UserCert(Base):
    """用户凭证信息表
    username：用户名
    password：用户密码
    capath：人员证书位置
    serial：人员证书的序列号
    rgbimgpath：人脸图片存储位置
    """
    # 定义表名
    __tablename__ = 'user_cert'
    # 定义列对象
    username = Column(String(256), primary_key=True)
    password = Column(String(256))
    capath = Column(String(256))
    serial = Column(String(256))
    rgbimgpath = Column(String(256))


if __name__ == "__main__":
    print("初始化，创建所有表!")
    # Base.metadata.create_all(db_engine)  # 创建本文件定义的所有表
    Base.metadata.create_all(test_db_engine)  # 创建本文件定义的所有表
