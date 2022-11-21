#-*- coding:UTF-8 -*-

import logging
from socket import *
import sys

def tcp_utils(host,port,msg):

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
    tcpClient.send(bytes.fromhex(info))
    # 关闭链接
    tcpClient.close()

if __name__ == '__main__':
    tcp_utils('','',"a55a00003b485a5453323230383030303534c8003c000a0101006401f400096279FD500009000900090009000900090009000900090009376A55aa")