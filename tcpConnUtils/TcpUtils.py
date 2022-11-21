#-*- coding:UTF-8 -*-

import logging
from socket import *
import sys

def tcp_utils(host,port,msg):

    # host = "192.168.0.214"
    # port = 7895
    addr = (str(host), int(port))
    tcpClient = socket(AF_INET, SOCK_STREAM)
    try:
        remote_ip = gethostbyname(host)
    except gaierror:
        # could not resolve
        logging.info('Hostname could not be resolved. Exiting')
        sys.exit()
    print('Ip address of ' + host + ' is ' + remote_ip)
    tcpClient.connect(addr)
    logging.info('connetion success...')
    logging.info(tcpClient.getpeername())
    #info = "a55a00003b485a5453323230383030303534c8003c000a0101006401f400096279FD500009000900090009000900090009000900090009376A55aa"
    info = msg
    tcpClient.send(bytes.fromhex(info))
    tcpClient.close()

if __name__ == '__main__':
    tcp_utils('','',"a55a00003b485a5453323230383030303534c8003c000a0101006401f400096279FD500009000900090009000900090009000900090009376A55aa")