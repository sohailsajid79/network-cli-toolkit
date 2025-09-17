# Network Calculator CLI

![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python)
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)

A Python CLI for working with IPs, subnetting, CIDR calculations, and cloud networking (AWS, Azure, etc.).

## Features
- CIDR input → network, broadcast, first/last usable host
- Subnet mask to CIDR converter
- CIDR prefix → host capacity for General / AWS / Azure
- CIDR range table CSV generator
- IP address lookup: class, public/private, loopback

## Installation
### Local via `pip install .`
```bash
git clone https://github.com/sohailsajid79/network-cli-toolkit.git
cd network-cli-toolkit
pip install .
```

## Dev Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

## Docker
```bash
docker build -t netcli .
docker run --rm netcli subnet-info -ip 192.168.1.0/24
```

## Usage
### View Subnet Info
```bash
netcli subnet-info -ip 192.168.1.0/24
```

### Convert Subnet Mask to CIDR
```bash
netcli mask-to-cidr -sm 255.255.255.0
```

### Show Host Capacity for CIDR Prefix
```bash
netcli cidr-hosts -cidr 22
```

### IP Address Lookup
```bash
netcli ip-lookup -ip 8.8.8.8
```

### Generate Full CIDR Table (CSV)
```bash
netcli generate-cidr-table -o data/cidr_table.csv
```

## GitHub Actions
CI is configured via `.github/workflows/test.yml`:
- Runs pytest
- Installs tool and dev dependencies
- Ensures code quality for each push and PR