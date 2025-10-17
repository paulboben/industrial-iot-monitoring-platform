import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modbus_mqtt_gateway.core import main

if __name__ == "__main__":
    main()