from pyModbusTCP.client import ModbusClient

def read_coils(host, unit, start=0, count=10):
    """
    Read coils from a Modbus device using pyModbusTCP.
    Synchronous method (pyModbusTCP is synchronous).
    """
    client = ModbusClient(host=host, port=502, unit_id=unit, auto_open=True)
    coils = client.read_coils(start, count)
    if coils is None:
        print(f"Failed to read coils from {host}")
    return coils