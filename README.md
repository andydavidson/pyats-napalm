# pyats-napalm

An example showing how I managed to implement `pyats` to use Napalm instead of Genie/Unicon to connect to a Juniper device and run a check.  We are testing this at Ting Fiber.  The lack of BGP parsers for Junos in the native distribution made me search around for some other option vs writing our own.

The check I reimplemented was originally written by Kevin Corbin.

Flaws:
  * The router password doesn't load from the Testbed file, so I have hard coded it for this example
  * The napalm connection object sits in the very handy 'custom' pyats Device dictionary

As a proof of concept it works well

```
jump-eve:~/pyats/neighbor_check$ python ./BGP_Neighbors_Established.py 
2020-07-09T17:09:34: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:34: %AETEST-INFO: |                            Starting common setup                             |
2020-07-09T17:09:34: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:34: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:34: %AETEST-INFO: |                         Starting subsection connect                          |
2020-07-09T17:09:34: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:35: %AETEST-INFO: The result of subsection connect is => PASSED
2020-07-09T17:09:35: %AETEST-INFO: The result of common setup is => PASSED
2020-07-09T17:09:35: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:35: %AETEST-INFO: |                 Starting testcase BGP_Neighbors_Established                  |
2020-07-09T17:09:35: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:35: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:35: %AETEST-INFO: |                          Starting section learn_bgp                          |
2020-07-09T17:09:35: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:36: %AETEST-INFO: The result of section learn_bgp is => PASSED
2020-07-09T17:09:36: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:36: %AETEST-INFO: |                          Starting section check_bgp                          |
2020-07-09T17:09:36: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:36: %SCRIPT-ERROR: {
2020-07-09T17:09:36: %SCRIPT-ERROR:    "br01-eve-asva01": {
2020-07-09T17:09:36: %SCRIPT-ERROR:       "4.4.4.4": {
2020-07-09T17:09:36: %SCRIPT-ERROR:          "local_as": 32133,
2020-07-09T17:09:36: %SCRIPT-ERROR:          "remote_as": 15348,
2020-07-09T17:09:36: %SCRIPT-ERROR:          "remote_id": "",
2020-07-09T17:09:36: %SCRIPT-ERROR:          "is_up": false,
2020-07-09T17:09:36: %SCRIPT-ERROR:          "is_enabled": true,
2020-07-09T17:09:36: %SCRIPT-ERROR:          "description": "",
2020-07-09T17:09:36: %SCRIPT-ERROR:          "uptime": 261344,
2020-07-09T17:09:36: %SCRIPT-ERROR:          "address_family": {
2020-07-09T17:09:36: %SCRIPT-ERROR:             "ipv4": {
2020-07-09T17:09:36: %SCRIPT-ERROR:                "received_prefixes": -1,
2020-07-09T17:09:36: %SCRIPT-ERROR:                "accepted_prefixes": -1,
2020-07-09T17:09:36: %SCRIPT-ERROR:                "sent_prefixes": -1
2020-07-09T17:09:36: %SCRIPT-ERROR:             },
2020-07-09T17:09:36: %SCRIPT-ERROR:             "ipv6": {
2020-07-09T17:09:36: %SCRIPT-ERROR:                "received_prefixes": -1,
2020-07-09T17:09:36: %SCRIPT-ERROR:                "accepted_prefixes": -1,
2020-07-09T17:09:36: %SCRIPT-ERROR:                "sent_prefixes": -1
2020-07-09T17:09:36: %SCRIPT-ERROR:             }
2020-07-09T17:09:36: %SCRIPT-ERROR:          }
2020-07-09T17:09:36: %SCRIPT-ERROR:       }
2020-07-09T17:09:36: %SCRIPT-ERROR:    }
2020-07-09T17:09:36: %SCRIPT-ERROR: }
2020-07-09T17:09:36: %AETEST-ERROR: Failed reason: Testbed has BGP Neighbors that are not established
2020-07-09T17:09:36: %AETEST-INFO: The result of section check_bgp is => FAILED
2020-07-09T17:09:36: %AETEST-INFO: The result of testcase BGP_Neighbors_Established is => FAILED
2020-07-09T17:09:36: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:36: %AETEST-INFO: |                           Starting common cleanup                            |
2020-07-09T17:09:36: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:36: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:36: %AETEST-INFO: |                     Starting subsection clean_everything                     |
2020-07-09T17:09:36: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:36: %AETEST-INFO: The result of subsection clean_everything is => PASSED
2020-07-09T17:09:36: %AETEST-INFO: The result of common cleanup is => PASSED
2020-07-09T17:09:36: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:36: %AETEST-INFO: |                               Detailed Results                               |
2020-07-09T17:09:36: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:36: %AETEST-INFO:  SECTIONS/TESTCASES                                                      RESULT   
2020-07-09T17:09:36: %AETEST-INFO: --------------------------------------------------------------------------------
2020-07-09T17:09:36: %AETEST-INFO: .
2020-07-09T17:09:36: %AETEST-INFO: |-- common_setup                                                          PASSED
2020-07-09T17:09:36: %AETEST-INFO: |   `-- connect                                                           PASSED
2020-07-09T17:09:36: %AETEST-INFO: |-- BGP_Neighbors_Established                                             FAILED
2020-07-09T17:09:36: %AETEST-INFO: |   |-- learn_bgp                                                         PASSED
2020-07-09T17:09:36: %AETEST-INFO: |   `-- check_bgp                                                         FAILED
2020-07-09T17:09:36: %AETEST-INFO: `-- common_cleanup                                                        PASSED
2020-07-09T17:09:36: %AETEST-INFO:     `-- clean_everything                                                  PASSED
2020-07-09T17:09:36: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:36: %AETEST-INFO: |                                   Summary                                    |
2020-07-09T17:09:36: %AETEST-INFO: +------------------------------------------------------------------------------+
2020-07-09T17:09:36: %AETEST-INFO:  Number of ABORTED                                                            0 
2020-07-09T17:09:36: %AETEST-INFO:  Number of BLOCKED                                                            0 
2020-07-09T17:09:36: %AETEST-INFO:  Number of ERRORED                                                            0 
2020-07-09T17:09:36: %AETEST-INFO:  Number of FAILED                                                             1 
2020-07-09T17:09:36: %AETEST-INFO:  Number of PASSED                                                             2 
2020-07-09T17:09:36: %AETEST-INFO:  Number of PASSX                                                              0 
2020-07-09T17:09:36: %AETEST-INFO:  Number of SKIPPED                                                            0 
2020-07-09T17:09:36: %AETEST-INFO:  Total Number                                                                 3 
2020-07-09T17:09:36: %AETEST-INFO:  Success Rate                                                             66.7% 
2020-07-09T17:09:36: %AETEST-INFO: --------------------------------------------------------------------------------

```