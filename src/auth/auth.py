# -*- encoding:utf-8 -*-

from db.shared import DBSession
from db.tables import *
from usermanager import usermanager as um
from devicemanager import devicemanager as dm
from mytoken.mytoken import token_ins
from sm.sm import sm_ins
from conf import conf


# ========================外部接口========================== #
def user_verify(auth_dict):
    """用户名密码验证

    :param auth_dict: 用户信息，包含用户名、密码、设备ID
    :type auth_dict: dict
    :return: 执行结果代码
    :rtype: dict
    """

    ret_code = 0
    msg = "OK"

    username = auth_dict.get("username")
    password = auth_dict.get("password")
    devid = auth_dict.get("devID")
    session = DBSession()  # 创建数据库会话
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user is None:
        ret_code = 4001
        msg = "user not exist!"
        return {"ret_code": ret_code, "msg": msg}
    verify_data = user.password
    if not um.verify_password(password, verify_data):
        ret_code = 4002
        msg = "user verify fail!"
        return {"ret_code": ret_code, "msg": msg}

    # 身份认证成功，进行人机验证
    res = dm.user_dev_verify(auth_dict)
    if res["ret_code"] != 0:  # 人机验证失败
        return res

    # 人机验证成功，生成身份令牌
    ismi_token = token_ins.create_ismi_token(username, 600)  # 生成用户身份标识
    refresh_token = token_ins.create_ismi_token(username, 31536000)  # 生成用于刷新身份标识的令牌
    um.login(auth_dict)  # 登录成功

    return {"ret_code": ret_code, "msg": msg, "username": username, "ismi_token": ismi_token, "refresh_token": refresh_token}


def finger_verify(auth_dict):
    """指纹Ukey验证

    :param auth_dict: 用户信息，包含用户名、随机数、数字签名、设备ID
    :type auth_dict: dict
    :return: 执行结果代码
    :rtype: dict
    """

    ret_code = 0
    msg = "OK"

    realname = auth_dict.get("username")  # 电子钥匙中的用户名实际上是人名
    serial = auth_dict.get("serial")  # 证书序列号
    random = hexstring_bytes(auth_dict.get("random"))  # 随机数
    sign = hexstring_bytes(auth_dict.get("sign"))  # 签名数据
    devid = auth_dict.get("devID")
    print(devid, realname, serial, random.hex(), sign.hex())
    session = DBSession()  # 创建数据库会话
    user = session.query(UserCert).filter_by(serial=serial).first()
    session.close()
    if user is None:
        ret_code = 4001
        msg = "user not exist!"
        return {"ret_code": ret_code, "msg": msg}
    username = user.username
    pubfile = conf.pubkey_dir + "/" + realname + "_" + serial + ".cer"
    if not sm_ins.sm.verifySign(pubfile, random, sign):
        ret_code = 4004
        msg = "finger verify fail!"
        return {"ret_code": ret_code, "msg": msg}

    # 身份认证成功，进行人机验证
    auth_dict["username"] = username  # 改成用户账号名
    res = dm.user_dev_verify(auth_dict)
    if res["ret_code"] != 0:  # 人机验证失败
        return res

    # 人机验证成功，生成身份令牌
    ismi_token = token_ins.create_ismi_token(username, 600)  # 生成用户身份标识
    refresh_token = token_ins.create_ismi_token(username, 31536000)  # 生成用于刷新身份标识的令牌
    # um.login(auth_dict)  # 登录成功

    return {"ret_code": ret_code, "msg": msg, "username": username, "ismi_token": ismi_token, "refresh_token": refresh_token}


# ========================辅助函数========================== #
def bytes_hexstring(bs):
    """将bytes转换为16进制字符串
    :param bs:bytes
    :return: 16进制字符串，每个byte以空格分开
    """

    return ''.join(['%02X ' % b for b in bs])


def hexstring_bytes(hexstr):
    """将16进制字符串转换为bytes
    :param hexstr: 16进制字符串
    :return: bytes
    """
    hexstr = hexstr.replace(" ", "")
    return bytes.fromhex(hexstr)
