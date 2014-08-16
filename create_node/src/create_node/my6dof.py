#!/usr/bin/env python
# coding=utf-8
#
# Author: Yuanbo She yuanboshe@126.com
# Group: ExBot http://blog.exbot.net
#
# Software License Agreement (BSD License)
#
# Copyright (c) 2014, ExBot.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import rospy
import serial
import struct
import thread

class My6dof():
    def __init__(self, default_port='/dev/ttyUSB1'):
        self.port = default_port
        try:
            self.ser = serial.Serial(port=self.port, baudrate=115200, bytesize=8, stopbits=1)
            self.rpy = [0]*3
            thread.start_new_thread(self.update,())
#             while 1:
#                 rpy = self.read()
#                 print rpy
        except:
            print "Cant open serial port %s, please retry!"%self.port
    
    def update(self):
        while 1:
            if self.ser.read().encode('hex') == 'a5' and self.ser.read().encode('hex') == '5a' and int(self.ser.read().encode('hex'), 16) > 0 and self.ser.read().encode('hex') == 'a1':
                data = self.ser.read(6)
                rpy_raw = struct.Struct(">6B").unpack(data)
                rpy = [0]*3
                for i in range(3):
                    raw = 256 * rpy_raw[i*2] + rpy_raw[i*2+1]
                    if raw > 32768:
                        raw = 32768 - raw
                    rpy[i] = raw * 0.1
                self.rpy = rpy
            

    def read(self):
        return self.rpy

if __name__ == '__main__':
    My6dof()