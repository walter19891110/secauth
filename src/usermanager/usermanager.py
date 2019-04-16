# -*- encoding:utf-8 -*-

# 用户管理模块
from db.shared import DBSession
from db.tables import *
import time
from passlib.apps import custom_app_context as pwd_context


def encrypt_password(password):
    """密码散列

    :param password: 明文密码
    :param password: str
    :return 密文密码
    :rtype: str
    """

    return pwd_context.hash(password)


def verify_password(password, en_password):
    """对明密文密码进行验证

    :param password: 明文密码
    :param en_password: 密文密码
    :return: 密码正确返回True，密码错误返回False验证结果
    :rtype: Bool
    """

    ret = False
    try:
        ret = pwd_context.verify(password, en_password)
    except Exception as e:
        print(type(password), type(en_password), e)
    return ret


def add_user(user_dict):
    """添加用户

    :param user_dict: 用户信息
    :type : dict
    :return: 执行结果代码
    :rtype: dict
    """

    ret_code = 0
    msg = "OK"

    username = user_dict.get("username")
    session = DBSession()  # 创建数据库会话
    if session.query(User).filter_by(username=username).first() is not None:
        ret_code = 2002
        msg = "username already exist!"
        return {"ret_code": ret_code, "msg": msg}
    else:
        user = User(username=username)
        user.password = encrypt_password(user_dict.get("password"))
        user.userrole = user_dict.get("userrole")
        user.range = user_dict.get("range")
        user.realname = user_dict.get("realname")
        user.groupID = user_dict.get("groupID")
        user.orgID = user_dict.get("orgID")
        user.phone = user_dict.get("phone")
        session.add(user)
        session.commit()
    session.close()

    return {"ret_code": ret_code, "msg": msg}


def modify_user(user_dict):
    """修改用户信息

    :param user_dict: 用户信息
    :type user_dict: dict
    :return: 执行结果代码
    :rtype: dict
    """

    ret_code = 0
    msg = "OK"
    username = user_dict.get("username")

    session = DBSession()  # 创建数据库会话
    user = session.query(User).filter_by(username=username).first()
    if user is None:
        ret_code = 2002
        msg = "user not exist!"
        return {"ret_code": ret_code, "msg": msg}

    user.userrole = user_dict.get("userrole")
    user.range = user_dict.get("range")
    user.realname = user_dict.get("realname")
    user.groupID = user_dict.get("groupID")
    user.orgID = user_dict.get("orgID")
    user.phone = user_dict.get("phone")
    session.commit()
    session.close()

    return {"ret_code": ret_code, "msg": msg}


def modify_password(user_dict):
    """修改用户密码

    :param user_dict: 用户名，原密码，新密码
    :type user_dict: dict
    :return: 执行结果代码
    :rtype: dict
    """

    ret_code = 0
    msg = "OK"
    username = user_dict.get("username")

    session = DBSession()  # 创建数据库会话
    user = session.query(User).filter_by(username=username).first()
    if user is None:
        ret_code = 2002
        msg = "user not exist!"
        return {"ret_code": ret_code, "msg": msg}
    old_password = user_dict.get("oldpwd")
    new_password = user_dict.get("newpwd")
    if not verify_password(old_password, user.password):
        ret_code = 2003
        msg = "old password error!"
        return {"ret_code": ret_code, "msg": msg}

    user.password = encrypt_password(new_password)
    session.commit()
    session.close()

    return {"ret_code": ret_code, "msg": msg}


def del_user(user_dict):
    """删除用户信息

    :param user_dict: 用户名
    :type user_dict: dict
    :return: 执行结果代码
    :rtype: dict
    """

    ret_code = 0
    msg = "OK"
    username = user_dict.get("username")

    session = DBSession()  # 创建数据库会话
    user = session.query(User).filter_by(username=username).first()
    if user is None:
        ret_code = 2001
        msg = "user not exist!"
        return {"ret_code": ret_code, "msg": msg}

    session.delete(user)
    session.commit()
    session.close()

    return {"ret_code": ret_code, "msg": msg}


def get_user(user_name):
    """获取用户信息

    :param user_name: 用户名
    :type user_name: str
    :return: 执行结果代码和用户信息
    :rtype: dict
    """

    ret_code = 0
    msg = "OK"

    session = DBSession()  # 创建数据库会话
    user = session.query(User).filter_by(username=user_name).first()
    session.close()
    if user is None:
        ret_code = 2001
        msg = "user not exist!"
        return {"ret_code": ret_code, "msg": msg}

    return {"ret_code": ret_code, "msg": msg, "username": user.username, "userrole": user.userrole,
            "range": user.range, "realname": user.realname, "groupID": user.groupID, "orgID": user.orgID,
            "phone": user.phone}


def login(user_dict):
    """登录成功，更新登录状态

    :param user_dict: 用户名
    :type user_dict: dict
    :return: 执行结果代码
    :rtype: dict
    """

    ret_code = 0
    msg = "OK"
    user_name = user_dict.get("username")

    # 更新登录状态
    session = DBSession()  # 创建数据库会话
    user_login = session.query(UserLogin).filter_by(username=user_name).first()

    if user_login is None:
        # 首次登录，写入数据库
        user_login = UserLogin(username=user_name)
        user_login.loginstatus = 0  # 登录成功
        user_login.logintime = time.strftime("%Y-%m-%dT%X", time.localtime(time.time()))
        user_login.loginhost = user_dict.get("devID")
        session.add(user_login)
        session.commit()
    else:
        if user_login.loginstatus == 1:
            user_login.loginstatus = 0
            session.commit()
        else:
            ret_code = 2003
            msg = "user already logined!"
            return {"ret_code": ret_code, "msg": msg}

    session.close()

    return {"ret_code": ret_code, "msg": msg}


def logout(user_dict):
    """登录成功，更新登录状态

    :param user_dict: 用户名
    :type user_dict: dict
    :return: 执行结果代码
    :rtype: dict
    """

    ret_code = 0
    msg = "OK"
    user_name = user_dict.get("username")

    # 更新登录状态
    session = DBSession()  # 创建数据库会话
    user_login = session.query(UserLogin).filter_by(username=user_name).first()

    if user_login is None:
        ret_code = 2002
        msg = "user not exist!"
        return {"ret_code": ret_code, "msg": msg}
    else:
        if user_login.loginstatus == 0:
            user_login.loginstatus = 1  # 退出登录
            session.commit()
        else:
            ret_code = 2003
            msg = "user already logouted!"
            return {"ret_code": ret_code, "msg": msg}

    session.close()

    return {"ret_code": ret_code, "msg": msg}


def get_login_status(user_dict):
    """查询用户登录状态

    :param user_dict: 用户名
    :type: dict
    :return: 返回登录状态
    :rtype: dict
    """

    print("def get_login_status:", user_dict)
    return {"ret_code": 0, "msg": "df"}


# ========================外部接口========================== #
def add_user_cert(user_dict):
    """添加用户

    :param user_dict: 用户凭证信息
    :type : dict
    :return: 执行结果代码
    :rtype: dict
    """

    ret_code = 0
    msg = "OK"

    username = user_dict.get("username")
    session = DBSession()  # 创建数据库会话
    if session.query(UserCert).filter_by(username=username).first() is not None:
        ret_code = 2002
        msg = "username already exist!"
        return {"ret_code": ret_code, "msg": msg}
    else:
        user = UserCert(username=username)
        user.password = encrypt_password(user_dict.get("password"))
        user.capath = user_dict.get("capath")
        user.serial = user_dict.get("serial")
        user.rgbimgpath = user_dict.get("rgbimgpath")
        session.add(user)
        session.commit()
    session.close()

    return {"ret_code": ret_code, "msg": msg}


if __name__ == "__main__":

    user_dict = dict()
    user_dict["username"] = "wangjing1"
    user_dict["password"] = "walter"
    user_dict["userrole"] = "admin"
    user_dict["range"] = 0
    user_dict["realname"] = "周媛"
    user_dict["groupID"] = "二次安防"
    user_dict["orgID"] = "北京科东"
    user_dict["phone"] = "15652998145"

    add_user(user_dict)

    login_dict = {"username": "wangjing", "devID": "192.168.1.15"}
    login(login_dict)

    print(get_user("wangjing"))

    user_cert_dict = dict()
    user_cert_dict["username"] = "wangjing"
    user_cert_dict["password"] = "walter"
    user_cert_dict["capath"] = "/home/ilog/admin"
    user_cert_dict["serial"] = "020000000000000000000000000000AB"
    user_cert_dict["rgbimgpath"] = "周媛"

    add_user_cert(user_cert_dict)
