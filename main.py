from core.packetfilter import PacketFilter
from core.logger import logger
from core.utils import get_ip, get_mac, Qmode
import logging
import argparse
import os
import sys

if os.geteuid() != 0:
    sys.exit("[!] Please run as root")

parser = argparse.ArgumentParser()

#add MITMf options
sgroup = parser.add_argument_group("netfilter", "Options for netfilter")
sgroup.add_argument("--log-level", type=str,choices=['debug', 'info'], default="info", help="Specify a log level [default: info]")
sgroup.add_argument("-F", "--filter", type=str, help='Filter to apply to incoming traffic')
sgroup.add_argument("-m", "--mode", type=str, help='Capture mode: i for Input, o for Output, f for Forward.')
sgroup.add_argument("-d", "--debug", action="store_true", default=False , help='Print debug information.')


if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

options = parser.parse_args()

#Set the log level
logger().log_level = logging.__dict__[options.log_level.upper()]

formatter = logging.Formatter("%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
log = logger().setup_logger("MITMf", formatter)

if options.filter:
    pfilter = PacketFilter(options.filter)
    print "|_ PacketFilter online"
    print "   |_ Applying filter {} to incoming packets".format(options.filter)
    if options.mode in ['i','o','f']:
        pfilter.set_mode(options.mode)
    if options.debug:
        pfilter.debug = True
    try:
        pfilter.start()
    except KeyboardInterrupt:
        pfilter.stop()


