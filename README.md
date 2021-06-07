# Random-Bytes
It generates candidate addresses and probes whether these addresses are active or not in each BGP prefix.

According to these patterns, we design Random-Bytes algorithm based on BGP prefixes to collect active addresses.
We define the 16 bits between two colons as double-bytes,
so IPv6 addresses can be showed by 8 double-byteses. As the
algorithm runs, the variable double-bytes position shifts to the right in order, in double-bytes steps. The position of address
in variable double-bytes is filled with 0000-ffff, and the other
double-bytes is 0. If the variable position is not the last double-bytes, then 0 or 1 will be filled into the last double-bytes.

 eg:2001:da8::/32
 
 extend in 6 cases:
 
 case1:112-128 low bytes =>2001:0da8:0000:0000:0000:0000:0000:[0000-ffff]
 case3:96-112  low bytes =>2001:0da8:0000:0000:0000:0000:[0000-ffff]:0000 or 2001:0da8:0000:0000:0000:0000:[0000-ffff]:0001
 case3:90-96   low bytes =>2001:0da8:0000:0000:0000:[0000-ffff]:0000:0000 or 2001:0da8:0000:0000:0000:[0000-ffff]:0000:0001
 case4:64-90   low bytes =>2001:0da8:0000:0000:[0000-ffff]:0000:0000:0000 or 2001:0da8:0000:0000:[0000-ffff]:0000:0000:0001
 case5:48-64   low bytes =>2001:0da8:0000:[0000-ffff]:0000:0000:0000:0000 or 2001:0da8:0000:[0000-ffff]:0000:0000:0000:0001
 case6:32-48   low bytes =>2001:0da8:[0000-ffff]:0000:0000:0000:0000:0000 or 2001:0da8:[0000-ffff]:0000:0000:0000:0000:0001
 
 
runing example:
python3 Random-Bytes.py --IPv6= local IPv6
