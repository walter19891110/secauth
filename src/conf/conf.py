# -*- encoding:utf-8 -*-

import os
from xml.dom import minidom

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "../.."))
conf_dir = os.path.join(parent_dir, "conf")
conf_file = os.path.join(conf_dir, "conf.xml")

doms = minidom.parse(conf_file)
root = doms.documentElement
cert_file = root.getElementsByTagName('cert.file')[0]
p12_file = cert_file.getElementsByTagName("p12.file")[0].firstChild.data
pubkey_dir = cert_file.getElementsByTagName("pubkey.dir")[0].firstChild.data
