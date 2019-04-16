# -*- encoding:utf-8 -*-

import socketserver
import time
import json
import socket
import devicemanager as dm
from usermanager import usermanager as um
from auth import auth
from mytoken.mytoken import token_ins


class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        conn = self.request  # 每个客户端的连接
        print(self.client_address[0] + ":" + str(self.client_address[1]) + "的连接已建立!")
        # conn.sendall(b"conn success!")  # 回复客户端连接已建立
        while True:
            recv = conn.recv(1024)
            if not recv:
                break
            json_data = str(recv, encoding='utf-8')
            data = json.loads(json_data)
            print("接收到的数据:", json_data)
            ret = {"ret_code": 0}
            for v in data.values():
                if v is None:
                    msg = "missing arguments!"
                    ret = {"ret_code": 1, "msg": msg}

            if ret["ret_code"] == 0:
                type = data["type"]  # 获取请求的服务类型码，根据不同的类型码，提供不同的服务
                # print(type)
                # 终端入网验证
                if type == "001001":  # 入网验证
                    ret = dm.devicemanager.dev_verify(data)
                elif type == "002001":  # 添加用户
                    ret = um.add_user(data)
                elif type == "004001":  # 用户密码验证
                    ret = auth.user_verify(data)
                elif type == "004002":  # 电子钥匙验证
                    ret = auth.finger_verify(data)
                elif type == "005001":  # 更新身份标识
                    ret = token_ins.update_token(data['refresh_token'])
                elif type == "005002":  # 验证身份标识
                    ret = token_ins.verify_token(data['ismi_token'])
                else:
                    time.sleep(5)
            print(ret)
            conn.sendall(bytes(str(json.dumps(ret)), encoding='utf-8'))   # 将结果返回客户端

    def finish(self):
        print(self.client_address[0] + ":" + str(self.client_address[1]) + "的连接已断开!\n")


def my_socketserver(ip, port):
    s1 = socketserver.ThreadingTCPServer((ip, port), MyServer)  # 多线程
    # s1 = socketserver.ForkingTCPServer((ip, port), MyServer)  # 多进程程
    s1.serve_forever()


"""
import gevent
from gevent import socket
from gevent import monkey

monkey.patch_all()  # 类似于python中的黑魔法，把很多模块的阻塞的变成非阻塞的，比如socket中的rece和send都变为不阻塞了
def my_server(ip, port):
    s = socket.socket()
    s.bind((ip, port))
    s.listen(15)  # 监听15个连接，超过了就排队
    while True:
        client, add = s.accept()
        print(add)
        gevent.spawn(handle_request, client)  # 通过gevent的启动一个协程，把客户端的socket对象传进去


def handle_request(s):
    try:
        while True:
            recv = s.recv(1024)
            if not recv:
                break
            json_data = str(recv, encoding='utf-8')
            data = json.loads(json_data)
            # print(self.client_address, json_data)
            ret = {"ret_code": 1}
            type = data["type"]  # 获取请求的服务类型码，根据不同的类型码，提供不同的服务
            # 终端入网验证
            if type == "001001":  # 入网验证
                ret = dm.devicemanager.dev_verify(data)
            elif type == "002001":  # 添加用户
                ret = um.add_user(data)
            elif type == "004001":  # 用户密码验证
                ret = auth.user_verify(data)
            else:
                time.sleep(5)

            # print(ret)
            s.sendall(bytes(str(json.dumps(ret)), encoding='utf-8'))   # 将结果返回客户端
    except Exception as e:
        print(e)
    finally:
        s.close()
"""

if __name__ == "__main__":

    ip = "192.100.10.234"
    hostname = socket.gethostname()
    # ip = socket.gethostbyname(hostname)
    port = 5050
    print("secauth Server is Started!")
    print("Server ip:", ip, "port:", port)
    my_socketserver(ip, port)
    # my_server(ip, port)
