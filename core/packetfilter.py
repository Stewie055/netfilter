from core.utils import set_ip_forwarding, iptables, Qmode
from core.logger import logger
from scapy.all import *
from traceback import print_exc
import nfqueue

formatter = logging.Formatter("%(asctime)s [PacketFilter] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
log = logger().setup_logger("PacketFilter", formatter)

class PacketFilter:

    def __init__(self, filter):
        self.filter = filter
        self.mode = None
        self.debug = False

    def set_mode(self,mode):
        self.mode = mode

    def start(self):
        set_ip_forwarding(1)
        iptables().NFQUEUE(self.mode)
        self.q = nfqueue.queue()
        self.q.open()
        self.q.bind(socket.AF_INET)
        self.q.set_callback(self.modify)
        self.q.create_queue(0)

        while True:
            self.q.try_run()
        print("stopped")

    def modify(self, i, payload):
        #log.debug("Got packet")
        data = payload.get_data()
        packet = IP(data)
        debug = self.debug
        try:
            execfile(self.filter)
        except Exception:
            log.debug("Error occurred in filter")
            print_exc()


    def stop(self):
        self.q.unbind(socket.AF_INET)
        self.q.close()
        set_ip_forwarding(0)
        iptables().flush()
        sys.exit('closing...')
