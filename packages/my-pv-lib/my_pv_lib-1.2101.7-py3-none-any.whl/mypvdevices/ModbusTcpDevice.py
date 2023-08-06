#!/usr/bin/python

import logging
from socket import gaierror
import threading
from pyModbusTCP.client import ModbusClient
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.ModbusDevice import ModbusDevice
from mypvdevices.DeviceDiscoverer import DeviceDiscoverer

RESOLVEHOSTERROR = 99

class ModbusTcpException(Exception):
    def __init__(self, msg, code):

        if code == None:
            msg="errorcode required"
            raise TypeError(msg)

        self.code = code
        self.message = msg
    def __str__(self):
        return repr(str(self.message) + ". Error-Code: " + str(self.code))

class ModbusTcpDevice(ModbusDevice):
    __devicetype__ = "ModbusTcpDevice"
    __mutex__ = threading.Lock()
    __modbusClient__ = None
    __host__ = None

    def __init__(self, serial):
        ModbusDevice.__init__(self, serial)

    def sethost(self, hostname):
        logging.debug(self.getidentifier() + " Setting host to " + str(hostname))

        if hostname == None:
            msg="hostname required"
            logging.debug(self.getidentifier() + ": " + str(msg))
            raise TypeError(msg)

        if not isinstance(hostname, str):
            msg="hostname hast to be a string"
            logging.debug(self.getidentifier() + ": " + str(msg))
            raise TypeError(msg)

        self.__host__ = hostname

        if self.__modbusClient__ == None:
            try:
                self.__modbusClient__ = ModbusClient(host=self.__host__, port=502, timeout=5, auto_open=True, auto_close=True)
            except ValueError:
                print("Error with host or port params")
        else:
            self.__modbusClient__.host(self.__host__)

    def readregisters(self, startregisteraddress, registerstoread):
        return self.__readregisters__(startregisteraddress, registerstoread)

    def __readregisters__(self, startregisteraddress, registerstoread):
        with self.__mutex__:
            registers = dict()
            if self.__modbusClient__ != None:
                logging.debug(self.getidentifier() + " Host: " + str(self.__modbusClient__.host()) + ": Reading " + str(registerstoread) +" registers starting with register "+ str(startregisteraddress))
                try:
                    modbus_response = self.__modbusClient__.read_holding_registers(startregisteraddress, registerstoread)
                    if modbus_response == None:
                        errorcode = self.__modbusClient__.last_error()

                        if errorcode == 2:
                            raise ModbusTcpException("Host not reachable " + str(self.__modbusClient__.host()), errorcode)
                        elif errorcode == 4:
                            raise ModbusTcpException("Invalid Registers " + str(startregisteraddress) + " " + str(registerstoread), errorcode)
                        else:
                            raise ModbusTcpException("Unknown Error. Error Code " + str(errorcode), errorcode)

                    logging.debug(self.getidentifier() + ": Host: " + str(self.__modbusClient__.host()) + ": Data: " + str(modbus_response))
                    for i in range(len(modbus_response)):
                        registers[startregisteraddress + i] = modbus_response[i]
                except gaierror as e:
                    logging.warning(self.getidentifier() + ": Host: " + str(self.__modbusClient__.host()) + ". Cannot resolve host: " + str(self.__modbusClient__.host()))
                    raise ModbusTcpException("Cannot resolve host. " + str(self.__modbusClient__.host()), RESOLVEHOSTERROR)
                
                except Exception as e:
                    logging.warning(self.getidentifier() + ": Host: " + str(self.__modbusClient__.host()) + " Modbus read error: " + str(e))
                    raise e
            else:
                logging.error(self.getidentifier() + ": no Modbus-Client ")
        return registers

    def __readregister__(self, registeraddress):
        with self.__mutex__:
            register = None
            if self.__modbusClient__ != None:
                logging.debug(self.getidentifier() + " Host: " + str(self.__modbusClient__.host()) + ": Reading register " + str(registeraddress))
                try:
                    modbus_response = self.__modbusClient__.read_holding_registers(registeraddress, 1)
                    if modbus_response == None:
                        errorcode = self.__modbusClient__.last_error()

                        if errorcode == 2:
                            raise ModbusTcpException("Host not reachable " + str(self.__modbusClient__.host()), errorcode)
                        elif errorcode == 4:
                            raise ModbusTcpException("Invalid Register " + str(registeraddress), errorcode)
                        else:
                            raise ModbusTcpException("Unknown Error. Error Code " + str(errorcode), errorcode)

                    logging.debug(self.getidentifier() + ": Host: " + str(self.__modbusClient__.host()) + ": Data: " + str(modbus_response))
                    register = modbus_response[0]
                except gaierror as e:
                    logging.warning(self.getidentifier() + ": Host: " + str(self.__modbusClient__.host()) + ". Cannot resolve host: " + str(self.__modbusClient__.host()))
                    raise ModbusTcpException("Cannot resolve host. " + str(self.__modbusClient__.host()), RESOLVEHOSTERROR)
                
                except Exception as e:
                    logging.warning(self.getidentifier() + ": Host: " + str(self.__modbusClient__.host()) + ". Modbus error: " + str(e))
                    raise e
            else:
                logging.error(self.getidentifier() + ": no Modbus-Client ")
        return register

    def __writeregister__(self, registerId, value):
        with self.__mutex__:
            if self.__modbusClient__ != None:
                try:
                    result = self.__modbusClient__.write_single_register(registerId, value)
                except gaierror as e:
                    logging.warning(self.getidentifier() + ": Host: " + str(self.__modbusClient__.host()) + ". Cannot resolve host: " + str(self.__modbusClient__.host()))
                    raise ModbusTcpException("Cannot resolve host. " + str(self.__modbusClient__.host()), RESOLVEHOSTERROR)
                except Exception as e:
                    logging.warning(self.getidentifier() + " Modbus Write Error: " + str(e))
                    raise e
                if result == None:
                    logging.warning(self.getidentifier() + " Cannot write register. Register " + str(registerId))
                    raise ModbusTcpException("Cannot write register " + str(registerId))
                
    def discoverDevice(self):
        try:
            return DeviceDiscoverer.instance().getipforserial(self.__serial__)
        except Exception as e:
            logging.warning(self.getidentifier() + " Cannot discover device " + str(self.__serial__) + ". Error: " + str(e))
            return None

# Entry Point     
if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(levelname)s[%(threadName)s:%(module)s|%(funcName)s]: %(message)s', level=logging.INFO)

    # serial = "1601242002040015"
    serial = "2001002006100016"
    correctip = "192.168.92.29"

    device = ModbusTcpDevice(serial)

    device.sethost("myhost")
    try:
        register = device.readRegister(2000)
        print(register)
    except Exception as e:
        pass

    device.sethost(correctip)
    try:
        register = device.readRegister(2000)
        print(register)
    except Exception as e:
        pass
    try:
        register = device.readRegister(1001)
        print(register)
    except Exception as e:
        print("error: " + str(e))
    device.sethost("192.168.92.26")
    try:
        register = device.readRegister(1001)
        print(register)
    except Exception as e:
        if e.code == 2:
            print("Fixing host")
            host = device.discoverDevice()
            if host != None:
                device.sethost(host)
            else:
                device.sethost(correctip)
    try:
        register = device.readRegister(1001)
        print(register)
    except Exception as e:
        if e.code == 2:
            print("host cannot be fixed")

    try:    
        registers = device.readregisters(1000, 80)
        print(str(registers))
    except Exception as e:
        print("error: " + str(e))

    device.sethost("ggjgjg")
    try:
        registers = device.readregisters(1000, 80)
        print(str(registers))
    except Exception as e:
        print("nix geht")
    
    try:
        device.writeregister(1000, 55)
    except Exception as e:
        print("wieder nix")

    try:
        device.writeregister(2000, 55)
    except Exception as e:
        print("wieder nix")

    device.sethost("192.168.92.29")
    try:
        device.writeregister(2000, 55)
    except Exception as e:
        print("wieder nix")

    # print(str(device.getsetup()))

    # print(str(device.getData()))

    # print(str(device.getLogData()))