
#coding:utf-8
import os
import random
import zmapscan
import os
import ipaddress
from copy import deepcopy
import argparse
ipv6countALL=0
def Random_LowBytes_Extend(bgp_prefix):
    '''
    Function:
        probe the space of BGP prefix used random lowbytes
    Args:
        bgp_prefix : the target BGP prefix 
    Return:
        the result store the file that named by BGP prefix

    '''
    print("begin to probe in {} bgp prefix".format(bgp_prefix))
    global ipv6countALL
    ipv6pre=[]
    prefix=bgp_prefix.split("/")
    bgp=prefix[0]
    bgpcopy=deepcopy(bgp)
    prefix_space=int(prefix[1])
    #bgp prefix used 0 filled eg:2001:da8::/32 =>2001:0da8:0000:0000:0000:0000:0000:0000
    bgp=ipaddress.IPv6Address(bgp)
    bgp=bgp.exploded
    # eg:2001:da8::/32
    # extend in 5 cases:
    # case1:112-128 low bytes  =>2001:0da8:0000:0000:0000:0000:0000:0000-2001:0da8:0000:0000:0000:0000:0000:ffff
    # case3:96-112  low bytes  =>2001:0da8:0000:0000:0000:0000:0000:0000-2001:0da8:0000:0000:0000:0000:ffff:0000 or 2001:0da8:0000:0000:0000:0000:0000:0000-2001:0da8:0000:0000:0000:0000:ffff:0001
    # case3:90-96   low bytes  =>2001:0da8:0000:0000:0000:0000:0000:0000-2001:0da8:0000:0000:0000:ffff:0000:0000 or 2001:0da8:0000:0000:0000:0000:0000:0000-2001:0da8:0000:0000:0000:ffff:0000:0001
    # case4:64-90   low bytes  =>2001:0da8:0000:0000:0000:0000:0000:0000-2001:0da8:0000:ffff:0000:0000:0000:0000 or 2001:0da8:0000:0000:0000:0000:0000:0000-2001:0da8:0000:ffff:0000:0000:0000:0001
    # case5:32-48   low bytes  =>2001:0da8:0000:0000:0000:0000:0000:0000-2001:0da8:ffff:0000:0000:0000:0000:0000 or 2001:0da8:0000:0000:0000:0000:0000:0000-2001:0da8:ffff:0000:0000:0000:0000:0001
    
    # store the bgp by list which can changed by later
    bgp=bgp.split(":")
    if prefix_space%4!=0:
        prefix_space=(int(prefix_space/16)+1)*16   
    while prefix_space<112:
        position=prefix_space/16
        for i in range(2**16):
            nybble_4=str(hex(i))[2:]
            ip=""
            for j in range(8):
                if j!=position and j<7:
                    ip=ip+bgp[j]+":"
                elif j!=7:
                    ip=ip+nybble_4+":"
                else:
                    iptemp=deepcopy(ip)
                    ip=ip+"0000"
                    ip=ipaddress.IPv6Address(ip)
                    ipv6pre.append(ip)
                    iptemp=iptemp+"0001"
                    iptemp=ipaddress.IPv6Address(iptemp)
                    ipv6pre.append(iptemp)

        prefix_space+=16
    for i in range(2**16):
        nybble_4=str(hex(i))[2:]
        ip=""
        for j in range(7):
            ip=ip+bgp[j]+":"
        ip=ip+nybble_4
        ip=ipaddress.IPv6Address(ip)
        ipv6pre.append(ip)

    # store the result
    prefile="extendLowBytes/result.csv"
    with open(prefile,'w') as f:
        for line in ipv6pre:
            f.write(str(line)+"\n")
    activefile="extendLowBytes/"+"active.csv"
    ipv6local=args.ipv6
    zmapscan.IPv6activeScan(ipv6local, prefile, activefile)
    command='wc -l '+activefile
    v6_result=os.popen(command)
    hited_number=float(v6_result.read().split()[0])
    v6_result.close()
    command="rm -rf "+prefile
    os.system(command)
    if hited_number==0:
        command="rm -rf "+activefile
        os.system(command)
    else:
        ipv6list=set()
        for line in open(activefile):
            line=line.replace("{","")
            line=line.replace("}","").strip().split(": ")[1].replace("\"","").replace("\"","")
            #print(line)
            ipv6list.add(line)
        y=len(ipv6list)
        ipv6countALL=ipv6countALL+y
        print("probe the prefix {},found {} ipv6 active address".format(bgp_prefix,y))
        print("now we total fonud ipv6 address is :{}".format(ipv6countALL))
        with open(activefile,'w') as f:
            for ipv6 in ipv6list:
                f.write(ipv6+"\n")
       


if __name__ == "__main__":
    parse=argparse.ArgumentParser()
    parse.add_argument('--ipv6', type=str, help='the host of running pro counts')
    args=parse.parse_args()
    Random_LowBytes_Extend("2001:16a2::/32")
