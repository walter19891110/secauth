# -*- encoding:utf-8 -*-

from py4j.java_gateway import JavaGateway
from py4j.java_gateway import GatewayParameters
import json
import base64
import time
from conf import conf
from sm.sm import sm_ins


class MyToken(object):

    # def __init__(self):
    #     self.gateway = JavaGateway(gateway_parameters=GatewayParameters(port=25666))  # 连接Java网关
    #     self.sm = self.gateway.entry_point.getSm()
    #
    # def __del__(self):
    #     self.gateway.close()

    def create_token(self, payload, expires):
        """生成Token

        :param payload: 令牌中的明文信息,
        :type : dict
        :param expires: Token有效期，int型，单位s
        :type : int
        :return : 新生成的令牌
        :type : str
        """

        payload["createtime"] = int(time.time())
        payload["overtime"] = expires
        caname = conf.p12_file.split('/')[-1].split('.')[0]
        payload["caname"] = caname
        json_str = json.dumps(payload)
        base64_byte = base64.b64encode(json_str.encode("utf-8"))
        print("明文信息:", payload)

        p12file = conf.p12_file
        pwd = "1234"
        # signdata = self.sm.dataSign(p12file, pwd, base64_byte)  # 生成签名
        signdata = sm_ins.sm.dataSign(p12file, pwd, base64_byte)  # 生成签名
        # print("签名内容:", base64.b64encode(signdata))

        token = base64_byte + b'.' + base64.b64encode(signdata)  # 生成Token
        token_str = token.decode("utf-8")
        # print("生成的令牌:", token_str)
        return token_str

    def analysis_token(self, token):
        """解析令牌

        :param token: 待解析的令牌
        :type : str
        :return: 解析结果
            {"ret_code": 0,
             "msg": "OK",
             "username": token中的用户名,
             "userrole": token中的用户角色
            }
        """

        ret = dict()
        ret["ret_code"] = 0
        ret["msg"] = "OK"

        try:
            token_list = token.split('.')
            payload = token_list[0].encode("utf-8")
            signdata = token_list[1].encode("utf-8")
            # print("payload:", payload)
            # print("signdata:", signdata)

            # 解析payload, 验证令牌是否过期
            payload_dict = json.loads(base64.b64decode(payload))
            create_time = payload_dict.pop("createtime")
            over_time = payload_dict.pop("overtime")
            ca_name = payload_dict["caname"]
            cur_time = int(time.time())
            if cur_time - create_time > over_time:
                ret["ret_code"] = 5001
                ret["msg"] = "Token expired!"

            # 没有过期，验签令牌
            pubfile = conf.pubkey_dir + "/pubkey_" + ca_name + ".crt"
            # res = self.sm.verifySign(pubfile, payload, base64.b64decode(signdata))
            res = sm_ins.sm.verifySign(pubfile, payload, base64.b64decode(signdata))
            print(res)
            if res is False:
                ret["ret_code"] = 5002
                ret["msg"] = "Verify Signature failed!"
                return ret

            # 验签成功，返回令牌内容
            for k, v in payload_dict.items():
                ret[k] = v
        except Exception as e:
            ret["ret_code"] = 5003
            ret["msg"] = "Wrong token with unknown reason!"
        # print("解析结果:", ret)
        return ret

    def verify_token(self, token):
        """验证令牌

        :param token: 待验证的令牌
        :type :str
        :return: 验证结果
            {"ret_code": 0,
             "msg": "OK"
            }
        """

        res = self.analysis_token(token)
        return {"ret_code": res.get("ret_code"), "msg": res.get("msg")}

    def update_token(self, refresh_token):
        """刷新令牌
           使用刷新令牌，生成新的访问令牌
        :param ref_token: 刷新令牌
        :type : str
        :return: 新的访问令牌
            {"ret_code": 0,
             "msg": "OK",
             "token": 新的访问令牌
            }
        """

        print(refresh_token)
        ret = self.verify_token(refresh_token)  # 验证令牌
        if ret.get("ret_code") is not 0:  # 如果res[0]不为0，说明令牌解析失败，返回错误码
            return ret

        # 令牌验证成功，生成新的令牌
        token_list = refresh_token.split('.')
        payload = token_list[0].encode("utf-8")
        payload_dict = json.loads(base64.b64decode(payload))
        payload_dict.pop("createtime")
        payload_dict.pop("overtime")
        ret["ismi_token"] = self.create_token(payload_dict, 600)
        return ret

    def create_ismi_token(self, username, expires):
        """生成用户身份标识

        :param username: 用户名
        :type : str
        :param expires: 超时时间
        :type : int
        :return:用户身份标识
        :type : str
        """
        payload = {"username": username}
        return self.create_token(payload, expires)

    def create_access_token(self, username, appid, expires):
        """生成用户身份标识

        :param username: 用户名
        :type : str
        :param appid: 业务系统ID
        :type : str
        :param expires: 超时时间
        :type : int
        :return:用户身份标识
        :type : str
        """
        payload = {"username": username, "appid": appid}
        return self.create_token(payload, expires)

    def create_remote_token(self, username, expires):
        """生成用户身份标识

        :param username: 用户名
        :type : str
        :param expires: 超时时间
        :type : int
        :return:用户身份标识
        :type : str
        """

        # 根据用户名查询所属的调度机构
        orgID = "江苏省调"
        payload = {"username": username, "orgid": orgID}
        return self.create_token(payload, expires)


token_ins = MyToken()

if __name__ == "__main__":
    print("令牌管理模块!")
    mytoken = MyToken()

    # 生成身份标识
    print("生成身份标识")
    ismi = mytoken.create_ismi_token("王景", 600)
    print("解析结果:", mytoken.analysis_token(ismi))

    # 生成访问令牌
    print("生成访问令牌")
    access = mytoken.create_access_token("王景", 123, 600)
    print("解析结果:", mytoken.analysis_token(access))

    # 生成广域访问令牌
    print("生成广域访问令牌")
    remote = mytoken.create_remote_token("王景", 600)
    print("解析结果:", mytoken.analysis_token(remote))
