# -*- encoding:utf-8 -*-

# 设备管理模块，实现终端入网验证和人机验证功能
from db.shared import DBSession
from db.tables import *


# ========================外部接口========================== #
def dev_verify(dev_dict):
    """
    终端入网验证

    :param dev_dict:
        设备信息
    :return:
        执行结果代码
        {"ret_code": ret_code, "msg": msg}
    """
    ret_code = 0
    msg = "OK"

    dev_id = dev_dict.get("devID")
    dev_ic = dev_dict.get("devIC")

    # 终端验证

    # 创建session对象，查询数据库
    session = DBSession()
    dev = session.query(DeviceInfo).filter_by(devID=dev_id).first()
    session.close()
    # dev = None
    if dev is None:
        ret_code = 1001
        msg = "dev not exist!"
        return {"ret_code": ret_code, "msg": msg}

    if dev_ic != dev.devIC:
        ret_code = 1002
        msg = "dev verify fail!"
        return {"ret_code": ret_code, "msg": msg}

    return {"ret_code": ret_code, "msg": msg}


def user_dev_verify(dev_dict):
    """人机验证

    :param dev_dict:设备信息，包含用户名、设备ID
    :return:
        执行结果代码
        {"ret_code": ret_code, "msg": msg}
    """

    ret_code = 0
    msg = "OK"

    dev_id = dev_dict.get("devID")
    user_name = dev_dict.get("username")

    # 人机验证
    session = DBSession()
    dev = session.query(DeviceInfo).filter_by(devID=dev_id).first()
    session.close()
    # dev = None
    if dev is None:
        ret_code = 6001
        msg = "dev not exist!"
        return {"ret_code": ret_code, "msg": msg}

    user_list = dev.userlist
    if not verify_user(user_name, user_list):
        ret_code = 6002
        msg = "user dev verify fail!"
        return {"ret_code": ret_code, "msg": msg}

    return {"ret_code": ret_code, "msg": msg}


def verify_user(username, userlist):
    if userlist is not None:
        user_list = userlist.split(',')
        for user in user_list:
            if user == username:
                return True
    return False
