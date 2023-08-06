"""Common verify functions for lacp"""

# Python
import re
import logging
import operator

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)


def verify_lacp_interface_receive_state(
    device, 
    interface, 
    expected_state,
    expected_interface=None,
    max_time=60,
    check_interval=10,
    ):
    """Verify the state of an lackp interface

    Args:
        device (obj): Device object
        interface (str): Interface name. Will be used if expected_interface isn't set
        expected_state (str): Expected state to check against. Defaults to None.
        expected_interface (str, optional): Expected interface to check against. Defaults to None.
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
    """

    interface_to_use = expected_interface if expected_interface else interface

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            cmd = 'show lacp interfaces {interface}'.format(interface=interface)
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # {
        # "lacp-interface-information-list": {
        #     "lacp-interface-information": {
        #         "lag-lacp-protocol": [
        #             {
        #                 "lacp-mux-state": "Collecting " "distributing",
        #                 "lacp-receive-state": "Current",
        #                 "lacp-transmit-state": "Fast " "periodic",
        #                 "name": "ge-0/0/0",
        #             },

        interfaces = out.q.get_values('lag-lacp-protocol')
        states = {intr['name']: intr['lacp-receive-state'] for intr in interfaces}

        if expected_state == states.get(interface_to_use, None):
            return True
        
        timeout.sleep()
    
    return False