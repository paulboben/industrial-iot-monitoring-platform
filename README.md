# Phase 1- Modbus–MQTT Edge Gateway — Setup Guide

A quick setup guide to run the Modbus simulator (Go) and the Python Modbus→MQTT edge gateway.  
Follow the sections below in order.

---

## 📁 Project Folder Structure

```
modbus-mqtt-edge/
├── modbus_mqtt_gateway/        # Python package (core, modbus_client, mqtt_client, utils, config)
│   ├── __init__.py
│   ├── core.py
│   ├── modbus_client.py
│   ├── mqtt_client.py
│   ├── utils.py
│   └── config.py
├── scripts/
│   └── run.py                  # Entry point to start the gateway
├── venv/                       # Python virtual environment (ignored in git)
├── docker-compose.yml           # Optional: MQTT broker or other services
├── modbus-server.go             # Go-based Modbus simulator
├── requirements.txt             # Python dependencies
└── README.md
```

---

## ⚙️ Prerequisites

- Ubuntu / Debian based system (or WSL Ubuntu)
- Python 3.11+ (`python3`, `pip`, and `python3-venv`)
- Go (for Modbus simulator)
- Docker / Docker Compose (optional, for Mosquitto)
- Git (optional)

---

## 1. Install Go (example: Go 1.25.3)

Download the Go tarball from [https://go.dev/dl/](https://go.dev/dl/)  
Then run:

```bash
# from your download folder
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.25.3.linux-amd64.tar.gz

# make Go available in the current shell
export PATH=$PATH:/usr/local/go/bin

# verify
go version
```

### Make Go available for `sudo`
To allow `sudo go run` without `command not found`:

```bash
sudo visudo
```

Append `/usr/local/go/bin` to the `secure_path` line, for example:
```
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/go/bin"
```

---

## 2. Run the Go-based Modbus Simulator

```bash
cd ~/iot-monitoring/devices
sudo go run modbus-server.go 502
```

> This starts the Modbus simulator on TCP port 502, emulating a Modbus server.

If Go is not in PATH for `sudo`, use:
```bash
sudo env "PATH=$PATH" go run modbus-server.go 502
```

---

## 3. Setup Python Virtual Environment

```bash
cd ~/iot-monitoring/devices/modbus-mqtt-edge

# remove any old venv
deactivate 2>/dev/null || true
rm -rf venv

# create new venv
python3 -m venv venv
source venv/bin/activate

# upgrade pip
pip install --upgrade pip
```

---

## 4. Install Python Dependencies

If you have a `requirements.txt` file:
```bash
pip install -r requirements.txt
```

Otherwise, manually install:
```bash
pip install pyModbusTCP paho-mqtt
```

> 🚫 Do **not** use `sudo` while in the virtual environment.

---

## 5. Setup Local MQTT Broker (Optional)

If you need a local MQTT broker (Mosquitto), use Docker:

```bash
sudo docker run -d --name mqtt5 -p 1883:1883 -p 9001:9001 eclipse-mosquitto
```

Or via `docker-compose.yml` (if included):
```bash
sudo docker compose up -d
```

Check if the broker is running:
```bash
sudo docker ps
ss -ltnp | grep 1883
```

---

## 6. Run the Modbus → MQTT Gateway

With your venv active:

```bash
python3 scripts/run.py
```

This script:
- Connects to the Modbus devices defined in `config.py`
- Reads coil/register values
- Formats them into JSON
- Publishes them to the configured MQTT topics

Stop the process anytime using `Ctrl + C`.

---

## 7. Troubleshooting



### Go command not found under sudo
Run:
```bash
sudo env "PATH=$PATH" go run modbus-server.go 502
```
or update `/etc/sudoers` with `/usr/local/go/bin` (as shown earlier).

---

### Docker network errors
If Docker Compose fails:
```bash
sudo docker-compose down -v
sudo docker network prune -f
sudo docker container prune -f
sudo docker-compose up -d
```

---

## 8. Helpful Commands

```bash
# show running containers
sudo docker ps

# list python packages
pip list

# check go version
go version

# check active ports
ss -ltnp | grep LISTEN
```

---

## 🧾 9. Notes

- Adjust file paths to match your environment.
- Keep `venv/` in `.gitignore` (don’t commit it).
- Update `config.py` with actual Modbus device IPs, unit IDs, and MQTT topics.
- Stop both simulator and gateway gracefully with `Ctrl + C`.

---

## 🪪 License

This repository is intended for development and testing purposes only.  
Use at your own discretion. Contributions and suggestions are welcome.

---

✅ **Setup Complete!**
You can now:
1. Start your Modbus simulator:
   ```bash
   sudo go run modbus-server.go 502
   ```
2. Run your Modbus → MQTT gateway:
   ```bash
   source venv/bin/activate
   python3 scripts/run.py
   ```
3. Watch data flow into your MQTT broker in real-time.
