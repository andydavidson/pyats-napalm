#!/bin/env python

# To get a logger for the script
import logging
import json
# To build the table at the end
from tabulate import tabulate

# Needed for aetest script
from ats import aetest
from ats.log.utils import banner

# Parse testbed file
from pyats.topology import loader, Device, Testbed

# Napalm Imports
from napalm import get_network_driver

# Get your logger for your script
log = logging.getLogger(__name__)

###################################################################
#                  COMMON SETUP SECTION                           #
###################################################################

class common_setup(aetest.CommonSetup):
    """ Common Setup section """

    # CommonSetup have subsection.
    # You can have 1 to as many subsection as wanted

    # Connect to each device in the testbed
    @aetest.subsection
    def connect(self):
        testbedfile = "../testbeds/eve.yaml"
        testbed = loader.load(testbedfile)
        device_list = []
        for device in testbed.devices:
            mydevice = testbed.devices[device]
            log.info(banner("Connect to device '{d}'".format(d=device)))
            log.info(banner("Running OS {o}".format(o=mydevice.type)))
            try:
                driver = get_network_driver(mydevice.type)
                mydevice.custom["napalmobj"] = driver(str(mydevice.connections['ssh']['ip']), str(testbed.credentials.default.username), "CHANGED")
                mydevice.custom["napalmobj"].open()
                device_list.append(mydevice)
            except Exception as e:
                self.failed("Failed to establish connection to '{}'".format(device))
                raise

        # Pass list of devices the to testcases
        self.parent.parameters.update(dev=device_list)


###################################################################
#                     TESTCASES SECTION                           #
###################################################################


class BGP_Neighbors_Established(aetest.Testcase):
    """ This is user Testcases section """

    # First test section
    @ aetest.test
    def learn_bgp(self):
        """ Sample test section. Only print """

        self.all_bgp_sessions = {}
        for dev in self.parent.parameters['dev']:
            our_bgp = dev.custom.napalmobj.get_bgp_neighbors()
            self.all_bgp_sessions[dev.name] = our_bgp["global"]["peers"] 

    @ aetest.test
    def check_bgp(self):
        """ Sample test section. Only print """

        failed_dict = {}
        mega_tabular = []
        for device, bgp in self.all_bgp_sessions.items():
            for nbr, props in bgp.items():
                state = props.get('is_up')
                tr = []
                if state == True:
                    tr.append(device)
                    tr.append(nbr)
                    tr.append("Established")
                    tr.append('Passed')
                else:
                    tr.append(device)
                    tr.append(nbr)
                    tr.append("Session down")
                    failed_dict[device] = {}
                    failed_dict[device][nbr] = props
                    tr.append('Failed')

                mega_tabular.append(tr)

        log.info(tabulate(mega_tabular,
                          headers=['Device', 'Peer',
                                   'State', 'Pass/Fail'],
                          tablefmt='orgtbl'))

        if failed_dict:
            log.error(json.dumps(failed_dict, indent=3))
            self.failed("Testbed has BGP Neighbors that are not established")

        else:
            self.passed("All BGP Neighbors are established")

# #####################################################################
# ####                       COMMON CLEANUP SECTION                 ###
# #####################################################################


# This is how to create a CommonCleanup
# You can have 0 , or 1 CommonCleanup.
# CommonCleanup can be named whatever you want :)
class common_cleanup(aetest.CommonCleanup):
    """ Common Cleanup for Sample Test """

    # CommonCleanup follow exactly the same rule as CommonSetup regarding
    # subsection
    # You can have 1 to as many subsections as wanted
    # here is an example of 1 subsection

    @aetest.subsection
    def clean_everything(self):
        """ Common Cleanup Subsection """
        log.info("Aetest Common Cleanup ")


if __name__ == '__main__':  # pragma: no cover
    aetest.main()
