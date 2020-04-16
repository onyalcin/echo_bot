import socket
import urllib.parse
import datetime
import logging
import time
from xml.etree import ElementTree as ET


logger = logging.getLogger(__name__)


class TCPSender:
    def __init__(self):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 8052
        self.BUFFER_SIZE = 1024
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = None

    def init_network(self):
        self.conn.connect((self.TCP_IP, self.TCP_PORT))

    def finit_network(self):
        self.conn.close()

    def send_msg(self, msg):
        str_id = '{:%M%S%f}'.format(datetime.datetime.now())
        self.conn.send(msg.encode())
        '''
        if self.data:
            self.data.append(self.conn.recv(self.BUFFER_SIZE))
        else:
            self.data = self.conn.recv(self.BUFFER_SIZE)
        '''
        return str_id

    def check_msg_done(self, str_id):
        logger.debug('Checking if msg done in Stopm')
        '''
        for msg in list(self.data):
            logger.debug('Listener Messages:%s\n', msg)
            if str_id in msg:
                logger.debug('Completed:%s\n', msg)
                self.data = None
                return True
            elif 'Remote+speech+process+timed+out' in msg[1]:
                self.data = None
                raise Exception
            self.data.remove(msg)  # FIXME: am i ugly?
        return False
        '''
        return True