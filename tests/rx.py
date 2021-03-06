#!/usr/bin/python
# Copyright: 2019, CCX Technologies

import socket
import ctypes
import ctypes.util
import struct
import fcntl
import sys

AF_AVIONICS = 18
PF_AVIONICS = 18
AVIONICS_RAW = 1

SIOCGIFINDEX = 0x8933

device = sys.argv[1]

def get_addr(sock, channel):
    data = struct.pack("16si", channel.encode(), 0)
    res = fcntl.ioctl(sock, SIOCGIFINDEX, data)
    idx, = struct.unpack("16xi", res)
    return struct.pack("Hi", AF_AVIONICS, idx)

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)

# == create socket ==
with socket.socket(PF_AVIONICS, socket.SOCK_RAW, AVIONICS_RAW) as sock:

    # == bind to interface ==
    # Python doesn't know about PF_ARINC so directly use libc
    addr = get_addr(sock, device)
    err = libc.bind(sock.fileno(), addr, len(addr))

    if err:
        raise OSError(err, "Failed to bind to socket")

    # == receive data example ==
    recv = sock.recv(4096)
    print(recv)
