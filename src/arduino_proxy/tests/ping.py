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

import glob
import logging
import optparse
import os
import sys
import time

# Setup PYTHONPATH
SRC_DIR = os.path.split(os.path.realpath(__file__))[0] # SRC_DIR/arduino_proxy/tests
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR/arduino_proxy
SRC_DIR = os.path.split(SRC_DIR)[0] # SRC_DIR
sys.path.append(os.path.abspath(SRC_DIR))

from arduino_proxy import ArduinoProxy

def main():
    parser = optparse.OptionParser(usage="usage: %prog [options] serial_device")
    parser.add_option("--debug",
        action="store_true", dest="debug", default=False,
        help="Show debug messages.")
    parser.add_option("--initial-wait",
        action="store", dest="initial_wait", default=None,
        help="How many seconds wait before conect (workaround for auto-reset on connect bug).")

    (options, args) = parser.parse_args()
    
    if len(args) == 0:
        parser.error("must specify the serial device (like /dev/ttyACM0). " + \
            "Serial devices that looks like Arduinos: %s." % ', '.join(glob.glob('/dev/ttyACM*')))
    elif len(args) > 1:
        parser.error("you specified more than one argument")
    
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)
    
    if options.initial_wait == 0:
        proxy = ArduinoProxy(args[0], 9600, wait_after_open=0)
    else:
        if options.initial_wait is None:
            print "Warning: waiting some seconds to let the Arduino reset..."
            proxy = ArduinoProxy(args[0], 9600)
        else:
            print "Warning: waiting %d seconds to let the Arduino reset..." % \
                int(options.initial_wait)
            proxy = ArduinoProxy(args[0], 9600, wait_after_open=int(options.initial_wait))
    try:
        while True:
            sys.stdout.write("Ping sent...")
            sys.stdout.flush()
            start = time.time()
            proxy.ping()
            end = time.time()
            sys.stdout.write(" OK - Time=%.3f ms\n" % ((end-start)*1000))
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        print ""
        proxy.close()

if __name__ == '__main__':
    main()
