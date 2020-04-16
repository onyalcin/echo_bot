import logging
from dialogue_system import bml
from .tcp_sender import TCPSender


logger = logging.getLogger().getChild(__name__)


class UnityBody:
    def __init__(self, character_name='ChrBrad'):
        self._conn = None
        self._character_name = character_name

    def __enter__(self):
        self._conn = TCPSender()
        self._conn.init_network()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.finit_network()

    def execute(self, bml_list):
        logger.debug('Executing BML commands:\n%s', bml_list)
        xml = bml.to_xml_clean(bml_list)
        logger.debug('Turning into XML:\n%s', xml)
        return self._conn.send_msg(xml)

    def check_done(self, id):
        logger.debug('MSG ID: %s', id)
        done = False
        while done == False:
            try:
                if self._conn.check_msg_done(id):
                    done = True
            except:
                done = True

    def execute_and_check(self, bml_list):
        logger.debug('Execute and Check in UnityBody')
        return self.check_done(self.execute(bml_list))
        #return self.execute(bml_list)