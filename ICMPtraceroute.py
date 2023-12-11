# Attribution: this assignment is based on ICMP Traceroute Lab from Computer Networking: a Top-Down Approach by Jim Kurose and Keith Ross. 
# It was modified for use in CSC249: Networks at Smith College by R. Jordan Crouser in Fall 2022

from socket import *
import socket
from ICMPpinger import checksum
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2

# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise
def build_packet():
    # In the sendOnePing() method of the ICMP Ping exercise, firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.

    #---------------#
    # Fill in start #
    #---------------#

    # TODO: Make the header in a similar way to the ping exercise. Append checksum to the header. 
    # (Solution can be implemented in 10 lines of Python code)
    
    #ICMP header fields 
    icmp_type = ICMP_ECHO_REQUEST
    icmp_checksum = 0
    icmp_code = 0
    icmp_id = os.getpid() & 0xFFFF
    icmp_seq = 1

    # Format header
    header = struct.pack("bbHHh", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)

    data = struct.pack("d", time.time())

    # Calculate checksum from header and data, then append
    icmp_checksum = checksum(''.join(map(chr, header + data))) # Correction from Bridget

    # Construct header with relevant checksum and information 
    header = struct.pack("bbHHh", icmp_type, icmp_code, htons(icmp_checksum), icmp_id, icmp_seq)

    #-------------#
    # Fill in end #
    #-------------#

    # Don’t send the packet yet , just return the final packet in this function.
    packet = header + data
    return packet

def get_route(hostname):
    timeLeft = TIMEOUT
    for ttl in range(1,MAX_HOPS):
        for tries in range(TRIES):
            destAddr = gethostbyname(hostname)

            #---------------#
            # Fill in start #
            #---------------#

            # TODO: Make a raw socket named mySocket. (Solution can be implemented in 2 lines of Python code)
            
            # Retrieve ICMP protocol number
            icmp = socket.getprotobyname("icmp")
            
            # Create raw socker
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

            #-------------#
            # Fill in end #
            #-------------#

            # Set TTL of packet
            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)

            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t= time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)

                if whatReady[0] == []: # Timeout
                    print(" * * * Request timed out.")

                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect

                if timeLeft <= 0:
                    print(" * * * Request timed out.")

            except timeout:
                continue

            else:
                #---------------#
                # Fill in start #
                #---------------#

                #TODO: Fetch the icmp type from the IP packet (Solution can be implemented in 2 lines of Python code)
                icmp_header = recvPacket[20:28]
                types, code, checksum, packet_id, sequence = struct.unpack("bbHHh", icmp_header)

                try:
                    # Get hostname from the received IP address
                    intermediate_host = gethostbyaddr(addr[0])
                    intermediate_hostname = intermediate_host[0]
                except herror:
                    intermediate_hostname = "Hostname not available"

                #-------------#
                # Fill in end #
                #-------------#
                
                if types == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 +bytes])[0]
                    print(" %d. %s, rtt=%.0f ms, %s" % (ttl, intermediate_hostname, (timeReceived - t) * 1000, addr[0]))
                elif types == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d. %s, rtt=%.0f ms, %s" % (ttl, intermediate_hostname, (timeReceived - t) * 1000, addr[0]))
                elif types == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d. %s, rtt=%.0f ms, %s" % (ttl, intermediate_hostname, (timeReceived - timeSent) * 1000, addr[0]))
                    return

                else:
                    print("error")

                break

            finally:
                mySocket.close()

# Runs program
if __name__ == "__main__":
    target = sys.argv[1]
    get_route(target)
