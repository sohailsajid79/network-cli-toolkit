import subprocess
import os
import ipaddress

def run_cli(args):
    result = subprocess.run(
        ["python", "network_tool.py"] + args,
        capture_output=True,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def test_subnet_info():
    stdout, stderr, code = run_cli(["subnet-info", "-ip", "10.0.0.0/24"])
    assert "Network Address" in stdout
    assert code == 0

def test_mask_to_cidr():
    stdout, stderr, code = run_cli(["mask-to-cidr", "-sm", "255.255.255.192"])
    assert "CIDR Notation" in stdout
    assert "/26" in stdout
    assert code == 0

def test_cidr_hosts():
    stdout, stderr, code = run_cli(["cidr-hosts", "-cidr", "22"])
    assert "Total Addresses" in stdout
    assert "Usable Hosts" in stdout
    assert code == 0

def test_cidr_host_count():
    net = ipaddress.ip_network("192.168.0.0/24")
    assert net.num_addresses == 256
    assert list(net.hosts())[0] == ipaddress.ip_address("192.168.0.1")

def test_generate_cidr_table():
    output_file = "cidr_sizes.csv"
    if os.path.exists(output_file):
        os.remove(output_file)

    try:
        stdout, stderr, code = run_cli(["generate-cidr-table", "-o", output_file])
        assert os.path.exists(output_file)
        assert "CIDR table saved" in stdout
        assert code == 0

    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

def test_ip_lookup():
    stdout, stderr, code = run_cli(["ip-lookup", "-ip", "8.8.8.8"])
    assert "IP Address" in stdout
    assert "Public" in stdout
    assert "IPv4" in stdout
    assert code == 0
