#-*- coding:UTF-8 -*-

import logging
import socket
import time
from socket import *
import sys

import serial


async def tcp_utils(host,port,msg):

    # host = "192.168.0.214"
    # port = 7895
    # 组装地址
    addr = (str(host), int(port))
    # 组装tcp链接
    tcpClient = socket(AF_INET, SOCK_STREAM)
    try:
        # 获取根据地址和名字布局的通讯链接
        remote_ip = gethostbyname(host)
    except gaierror:
        # could not resolve
        logging.info('Hostname could not be resolved. Exiting')
        # 发生异常则退出
        sys.exit()
    print('Ip address of ' + host + ' is ' + remote_ip)
    # 建立链接
    tcpClient.connect(addr)
    logging.info('connetion success...')
    logging.info(tcpClient.getpeername())
    #info = "a55a00003b485a5453323230383030303534c8003c000a0101006401f400096279FD500009000900090009000900090009000900090009376A55aa"
    info = msg
    # 发送消息
    # while True :
    #     tcpClient.send(bytes.fromhex(info))
    #     tc = tcpClient.recv(1024)
    #     tcpClient.send(tc)
    tcpClient.send(bytes.fromhex(info))

    # 关闭链接
    # tcpClient.close()


def tcp_con(host,port,msg):

    # host = "192.168.0.214"
    # port = 7895
    # 组装地址
    addr = (str(host), int(port))
    # 组装tcp链接
    tcpClient = socket(AF_INET, SOCK_STREAM)
    try:
        # 获取根据地址和名字布局的通讯链接
        remote_ip = gethostbyname(host)
    except gaierror:
        # could not resolve
        logging.info('Hostname could not be resolved. Exiting')
        # 发生异常则退出
        sys.exit()
    print('Ip address of ' + host + ' is ' + remote_ip)
    # 建立链接
    tcpClient.connect(addr)
    logging.info('connetion success...')
    logging.info(tcpClient.getpeername())
    print(tcpClient.getpeername())
    info = msg
    tcpClient.send(bytes.fromhex(info))
    time.sleep(1)
    # 关闭链接
    tcpClient.close()

if __name__ == '__main__':

    # tcp_con('47.110.73.94', '18893',
    #           '4040060001454D52323032333131340000FF0004000901000000D2616EA8B4CE9C2323')
    import os
    import sys
    # 当前文件的绝对路径
    current_file = os.path.abspath(os.getcwd())
    ps = os.path.abspath('2024-02-23-13-44-05-report.html')
    print(ps)
    # 当前文件所在的项目路径
    current_direct = os.path.dirname(current_file)
    # 项目根目录
    # project_root = os.path.dirname((os.path.dirname(current_direct)))
    print(current_direct)
    file_list = os.listdir(str(current_direct)+'\\report')
    print(file_list)
