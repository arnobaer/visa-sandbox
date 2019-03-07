# Basic instrument device class

import logging

class CoreDevice(object):

    def __init__(self, resource):
        self.resource = resource
        self.instr = None

    def connect(self, manager):
        logging.info("%s::connect(...)", self)
        self.instr = manager.get_instrument(self.resource)

    def valid(self):
        return self.instr is not None

    def write(self, command):
        logging.info("%s::write('%s')", self, command)
        return self.instr.write(command)

    def read(self,):
        logging.info("%s::read()", self)
        return self.instr.read()

    def query(self, command):
        logging.info("%s::query('%s')", self, command)
        return self.instr.query(command)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.resource)

class Device(CoreDevice):

    Q_IDN = '*IDN?'
    Q_SYSTEM_BEEPER_STATE = ':SYSTem:BEEPer:STATe?'
    W_SYSTEM_BEEPER_STATE_ON = ':SYSTem:BEEPer:STATe ON'
    W_SYSTEM_BEEPER_STATE_OFF = ':SYSTem:BEEPer:STATe OFF'

    def __init__(self, resource):
        super(Device, self).__init__(resource)

    def get_idn(self):
        return self.instr.query(self.Q_IDN).strip()

    def get_beeper(self):
        return self.instr.query(self.Q_SYSTEM_BEEPER_STATE).strip()

    def set_beeper(self, state):
        command = self.W_SYSTEM_BEEPER_STATE_ON if state else self.W_SYSTEM_BEEPER_STATE_OFF
        return self.instr.write(command)
