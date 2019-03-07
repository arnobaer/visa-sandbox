import visa

import argparse
import logging

from device import Device

logging.getLogger().setLevel(logging.INFO)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--driver', default='', help="Set VISA driver ('@py' to use pyVISA-py)")
    parser.add_argument('--list', action='store_true', help="list resources and exit")
    args = parser.parse_args()

    # Detect resources
    rm = visa.ResourceManager(args.driver)
    resources = rm.list_resources()

    if args.list:
        print(resources)
        return 0

    # Create some devices
    devices = [
        Device("GPIB1::15::INSTR"),
        Device("GPIB1::16::INSTR"),
    ]

    for device in devices:
        logging.info("********")
        if device.resource not in resources:
            logging.warning("%s not found", device)
        else:
            # Conenct with instrument
            device.connect(rm)
            logging.info("connected: %s", device.valid())
            # Get beeper state from device
            result = device.get_beeper()
            logging.info(result)
            # Get IDN from device
            result = device.get_idn()
            logging.info(result)
            # Query for IDN
            result = device.query("*IDN?")
            logging.info(result)
            # Write/read for IDN
            result = device.write("*IDN?")
            logging.info(result)
            result = device.read()
            logging.info(result)
            # Set beeper state to ON
            result = device.write(":SYSTem:BEEPer:STATe ON")
            logging.info(result)

    return 0

if __name__ == '__main__':
    main()
