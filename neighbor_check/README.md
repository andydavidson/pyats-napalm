# Overview

Reimplemented from https://github.com/kecorbin/pyats-network-checks/tree/master/bgp_adjacencies to use napalm instead

This check connects to all devices defined in the testbed, and parses BGP operational data.  The test passes if all BGP neighbors found are in the `established` state. 

# Running

```
python ./BGP_Neighbors_Established.py 
```

