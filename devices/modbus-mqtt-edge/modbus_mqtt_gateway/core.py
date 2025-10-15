import time
from .config import MODBUS_DEVICES, POLL_INTERVAL
from .modbus_client import read_coils
from .utils import format_payload

def main():
    try:
        while True:
            for device in MODBUS_DEVICES:
                coils = read_coils(device["host"], device["unit"])
                print(coils)
                if coils is not None:
                    payload = format_payload(coils)
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("Shutting down gateway...")