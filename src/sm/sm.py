# -*- encoding:utf-8 -*-

from py4j.java_gateway import JavaGateway
from py4j.java_gateway import GatewayParameters


class MySm(object):

    def __init__(self):
        self.gateway = JavaGateway(gateway_parameters=GatewayParameters(port=25666))  # 连接Java网关
        self.sm = self.gateway.entry_point.getSm()

    def __del__(self):
        self.gateway.close()


sm_ins = MySm()
