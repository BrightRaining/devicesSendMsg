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
        print(remote_ip)
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
    #info = "a55a00003b485a5453323230383030303534c8003c000a0101006401f400096279FD500009000900090009000900090009000900090009376A55aa"
    info = msg
    # 发送消息
    # while True :
    #     tcpClient.send(bytes.fromhex(info))
    #     tc = tcpClient.recv(1024)
    #     tcpClient.send(tc)
    tcpClient.send(bytes.fromhex(info))
    # 如果是数字电力就必须停止1s等待服务器响应
    time.sleep(1)
    # 关闭链接
    tcpClient.close()

if __name__ == '__main__':

    # ser = serial.Serial('COM6', 115200, timeout=1.5, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
    #                     bytesize=serial.EIGHTBITS)
    # senddata = '40400200014A4A31323334353637370080FF000100135C2A3CE51314004D0D3A0C580005A4000000008FBA2323'
    #
    # ser.write(bytes.fromhex(senddata))

    # sendAep("40400200014A4A31323334353637370080FF000100135C2A3CE51314004D0D3A0C580005A4000000008FBA2323")
    tcp_con('47.110.73.94', '18893',
              '4040060001454D52323032333131340000FF0004000901000000D2616EA8B4CE9C2323')
    # start_time = time.time()  # 记录程序开始运行时间
    # n = 0
    # for i in range(0,3000):
    #     n = i
    #     tcp_utils('47.110.73.94','17893','4040040013494132313039303039370070ff0004000e010a3dc511b3000000aa641aa1b680102323')
    # end_time = time.time()  # 记录程序结束运行时间
    # print('cost %f second' % (end_time - start_time))
    # print("发送成功: "+str(n))