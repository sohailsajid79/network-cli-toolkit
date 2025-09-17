#!/usr/bin/env python3

import argparse
import ipaddress
import csv
import os

def subnet_info(args):
    try:
        network = ipaddress.ip_network(args.ip, strict=False)
    except ValueError as e:
        print(f"[ERROR] Invalid CIDR: {e}")
        return

    print(f"\n--- Subnet Info for {args.ip} ---")
    print(f"Network Address     : {network.network_address}")
    print(f"Broadcast Address   : {network.broadcast_address}")
    print(f"Subnet Mask         : {network.netmask}")
    print(f"Wildcard Mask       : {ipaddress.IPv4Address(int(network.hostmask))}")
    print(f"CIDR Notation       : /{network.prefixlen}")
    print(f"Total Hosts         : {network.num_addresses}")
    usable = network.num_addresses - 2 if network.num_addresses > 2 else 0
    print(f"Usable Hosts        : {usable}")
    if usable > 0:
        hosts = list(network.hosts())
        print(f"First Usable Host   : {hosts[0]}")
        print(f"Last Usable Host    : {hosts[-1]}")
    print("----------------------------------------")

def mask_to_cidr(args):
    try:
        cidr = ipaddress.IPv4Network(f"0.0.0.0/{args.sm}").prefixlen
        print(f"\nSubnet Mask   : {args.sm}")
        print(f"CIDR Notation : /{cidr}")
    except ValueError as e:
        print(f"[ERROR] Invalid Subnet Mask: {e}")

def cidr_hosts(args):
    try:
        network = ipaddress.ip_network(f"0.0.0.0/{args.cidr}", strict=False)
    except ValueError as e:
        print(f"[ERROR] Invalid CIDR: {e}")
        return

    total = network.num_addresses
    usable_general = total - 2 if total > 2 else 0
    usable_cloud = total - 5 if total > 5 else 0

    print(f"\nCIDR: /{args.cidr}")
    print(f"Total Addresses       : {total}")
    print(f"Usable Hosts (General): {usable_general}")
    print(f"Usable Hosts (AWS)    : {usable_cloud}")
    print(f"Usable Hosts (Azure)  : {usable_cloud}")

def generate_cidr_table(args):
    output = args.output or "cidr_table.csv"

    os.makedirs(os.path.dirname(output), exist_ok=True)

    with open(output, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["CIDR", "Subnet Mask", "Total Hosts", "Usable (General)", "Usable (AWS)", "Usable (Azure)"])
        for prefix in range(8, 33):
            net = ipaddress.IPv4Network(f"0.0.0.0/{prefix}")
            total = net.num_addresses
            usable = total - 2 if total > 2 else 0
            usable_cloud = total - 5 if total > 5 else 0
            writer.writerow([f"/{prefix}", net.netmask, total, usable, usable_cloud, usable_cloud])
    print(f"\n✅ CIDR table saved to {output}")

def ip_lookup(args):
    try:
        ip = ipaddress.ip_address(args.ip)
        print(f"\nIP Address     : {ip}")
        print(f"Version        : IPv{ip.version}")
        print(f"Type           : {'Private' if ip.is_private else 'Public'}")
        print(f"Loopback       : {ip.is_loopback}")
        print(f"Multicast      : {ip.is_multicast}")
    except ValueError:
        print(f"[ERROR] Invalid IP address: {args.ip}")

def main():
    parser = argparse.ArgumentParser(prog="network_tool", description="IP Networking CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_subnet = subparsers.add_parser("subnet-info", help="CIDR input → network info")
    parser_subnet.add_argument("-ip", required=True, help="CIDR input (e.g., 192.168.1.0/24)")
    parser_subnet.set_defaults(func=subnet_info)

    parser_mask = subparsers.add_parser("mask-to-cidr", help="Convert subnet mask to CIDR")
    parser_mask.add_argument("-sm", required=True, help="Subnet mask (e.g., 255.255.255.0)")
    parser_mask.set_defaults(func=mask_to_cidr)

    parser_cidr = subparsers.add_parser("cidr-hosts", help="CIDR bits → total & usable hosts")
    parser_cidr.add_argument("-cidr", required=True, help="CIDR bits (e.g., 26)")
    parser_cidr.set_defaults(func=cidr_hosts)

    parser_table = subparsers.add_parser("generate-cidr-table", help="Generate CSV of CIDRs /8 to /32")
    parser_table.add_argument("-o", "--output", help="Output CSV file (default: cidr_table.csv)")
    parser_table.set_defaults(func=generate_cidr_table)

    parser_lookup = subparsers.add_parser("ip-lookup", help="Check IP type, version, class")
    parser_lookup.add_argument("-ip", required=True, help="IP address to inspect")
    parser_lookup.set_defaults(func=ip_lookup)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
