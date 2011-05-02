#!/usr/bin/env python
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    Py-Arduino-Proxy - Access your Arduino from Python
##    Copyright (C) 2011 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of Py-Arduino-Proxy.
##
##    Py-Arduino-Proxy is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    Py-Arduino-Proxy is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with Py-Arduino-Proxy; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import os
import sys

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy import ArduinoProxy, InvalidCommand, CommandTimeout
from arduino_proxy.tests import default_main

def main():
    options, args, proxy = default_main()
    try:
        print "connect() -> %s" % str(proxy.connect())
        print "ping() -> %s" % str(proxy.ping())
        print "pinMode() -> %s" % str(proxy.pinMode(13, ArduinoProxy.OUTPUT))
        print "analogRead() -> %s" % str(proxy.analogRead(0))
        print "analogWrite() -> %s" % str(proxy.analogWrite(0, 128))
        print "digitalRead() -> %s" % str(proxy.digitalRead(0))
        print "digitalWrite() -> %s" % str(proxy.digitalWrite(0, ArduinoProxy.HIGH))
        print "digitalRead() -> %s" % str(proxy.digitalRead(0))
        print "delay() -> %s" % str(proxy.delay(1))
        print "delayMicroseconds() -> %s" % str(proxy.delayMicroseconds(1))
        print "millis() -> %s " % str(proxy.millis())
        print "micros() -> %s" % str(proxy.micros())
        
        #define RETURN_OK 0
        #define READ_ONE_PARAM_NEW_LINE_FOUND 7
        #define READ_ONE_PARAM_EMPTY_RESPONSE 1
        #define READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE 2
        #define READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS 3
        #define UNEXPECTED_RESPONSE_FROM_READ_ONE_PARAM 4
        #define UNEXPECTED_RESPONSE_FROM_READ_PARAMETERS 5
        #define FUNCTION_NOT_FOUND 6
        
        try:
            print "Check for READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE"
            proxy.send_cmd("laaaarge_meeeethod_" * 10)
            assert False, "The previous line should raise an exception!"
        except InvalidCommand, e:
            # READ_ONE_PARAM_ERROR_PARAMETER_TOO_LARGE == 2
            print " +", e
            assert e.error_code == "2"

        try:
            print "Check for FUNCTION_NOT_FOUND"
            proxy.send_cmd("_nonexisting_method p1 p2 p3 p4 p5 p6 p7 p8 p9")
            assert False, "The previous line should raise an exception!"
        except InvalidCommand, e:
            # FUNCTION_NOT_FOUND == 6
            print " +", e
            assert e.error_code == "6"
        
        try:
            print "Check for READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS"
            proxy.send_cmd("cmd p1 p2 p3 p4 p5 p6 p7 p8 p9 p10")
            assert False, "The previous line should raise an exception!"
        except InvalidCommand, e:
            # READ_PARAMETERS_ERROR_TOO_MANY_PARAMETERS == 3
            print " +", e
            assert e.error_code == "3"
        
        proxy.setTimeout(1)
        print "delay(500)"
        proxy.delay(500)
        
        print "delay(1500)"
        try:
            proxy.delay(1500)
            assert False, "The previous line should raise an exception!"
        except CommandTimeout, e:
            print " +", e.__class__
        
        print "Re-connecting after timeout. connect() -> %s" % str(proxy.connect())
        
        #
        # Testing interrupt
        #
        
        #    LOW to trigger the interrupt whenever the pin is low,
        #    CHANGE to trigger the interrupt whenever the pin changes value
        #    RISING to trigger when the pin goes from low to high,
        #    FALLING for when the pin goes from high to low.
        #
        #    ATTACH_INTERRUPT_MODE_LOW = 'L'
        #    ATTACH_INTERRUPT_MODE_CHANGE = 'C'
        #    ATTACH_INTERRUPT_MODE_RISING = 'R'
        #    ATTACH_INTERRUPT_MODE_FALLING = 'F'
        
        print "proxy.pinMode()"
        proxy.pinMode(2, ArduinoProxy.INPUT)
        proxy.pinMode(3, ArduinoProxy.INPUT)
        proxy.delay(500)
        
        print "proxy.watchInterrupt(0)"
        print " +", proxy.watchInterrupt(0, ArduinoProxy.ATTACH_INTERRUPT_MODE_LOW)
        
        print "proxy.watchInterrupt(1)"
        print " +", proxy.watchInterrupt(1, ArduinoProxy.ATTACH_INTERRUPT_MODE_RISING)
        
        int0 = False
        int1 = False
        while int0 == False or int1 == False or True:
            if proxy.getInterruptMark(0):
                print " + INTERRUPT 0 has ocurred"
                int0 = True
            if proxy.getInterruptMark(1):
                print " + INTERRUPT 1 has ocurred"
                int1 = True
    
    except KeyboardInterrupt:
        print ""
    except Exception:
        raise
    finally:
        proxy.close()

if __name__ == '__main__':
    main()