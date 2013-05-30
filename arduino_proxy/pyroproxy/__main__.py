##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##    PyArduinoProxy - Access your Arduino from Python
##    Copyright (C) 2011-2012 - Horacio Guillermo de Oro <hgdeoro@gmail.com>
##
##    This file is part of PyArduinoProxy.
##
##    PyArduinoProxy is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 2.
##
##    PyArduinoProxy is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License version 2 for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with PyArduinoProxy; see the file LICENSE.txt.
##-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import hmac
import Pyro4

from arduino_proxy.proxy import ArduinoProxy


def main():
    """
    Expose object using PyRO
    """
    Pyro4.config.HMAC_KEY = hmac.new('this-is-PyArduinoProxy').digest()
    Pyro4.config.SOCK_REUSE = True
    proxy = ArduinoProxy()
    Pyro4.Daemon.serveSimple(
        {
            proxy: "arduino_proxy.Proxy",
            proxy.storage: "arduino_proxy.Storage",
        },
        host="localhost", port=61234, ns=False)
    # FORMA DE URI -> uri_string = "PYRO:arduino_proxy.Proxy@localhost:61234"

if __name__ == '__main__':
    main()