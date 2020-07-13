#!/usr/bin/python
# Multicast client
# Adapted from: http://chaos.weblogs.us/archives/164

import socket, os, re

ADDR = os.popen("ip route get 1 | fgrep src | sed 's@.*src \\([0-9\\.]\+\\).*@\\1@g'").read().strip()

LOCALPORT="6666"

ANY = "0.0.0.0"


# Use this if you want this to listen to ANY system instead of only the local system
# ADDR = ANY

MCAST_ADDR = "224.0.2.60"
MCAST_PORT = 4445

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Allow multiple sockets to use the same PORT number
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

# Bind to the port that we know will receive multicast data
sock.bind((ANY,MCAST_PORT))

# Tell the kernel that we want to add ourselves to a multicast group
# The address for the multicast group is the third param
status = sock.setsockopt(socket.IPPROTO_IP,
socket.IP_ADD_MEMBERSHIP,
socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY))

# setblocking(0) is equiv to settimeout(0.0) which means we poll the socket.
# But this will raise an error if recv() or send() can't immediately find or send data.
sock.setblocking(0)

currentPort = "0"

while 1:
    try:
        data, addr = sock.recvfrom(1024)
    except socket.error as e:
        pass
    else:
        if addr[0] == ADDR:
            print "Received ", ADDR, ": ", addr, " ---> ", data
            # data is a string of the form
            #  [MOTD]Player - Demo World[/MOTD][AD]41504[/AD]
            match = re.search('\[AD\](.+?)\[/AD\]', data)
            if match:
                newPort = match.group(1)

                if (newPort != currentPort):
                    print "NEW PORT:", newPort
                    currentPort=newPort

                    f = open("minecraftHaProxy.conf", "w")
                    f.write("# GENERATED CONFIG DON'T EDIT THIS MANUALLY\n")
                    f.write("\n")

                    f.write("defaults\n")
                    f.write("    timeout connect 5000\n")
                    f.write("    timeout client  5000\n")
                    f.write("    timeout server  5000\n")

                    f.write("frontend outside\n")
                    f.write("    bind :"+LOCALPORT+"\n")
                    f.write("    mode tcp\n")
                    f.write("    default_backend minecraft\n")

                    f.write("backend minecraft\n")
                    f.write("    server minecraft localhost:"+currentPort+"\n")
                    f.close()
                else:
                    print "Keeping existing port:", newPort, "==", currentPort

