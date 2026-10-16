#! /usr/bin/env python3

import argparse,platform,subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


def Helpmenu():         
    parser = argparse.ArgumentParser(description="PingSweeper")
    parser.add_argument("network", help="Example: pingsweeper 192.168.100.0/24")
    parser.add_argument("-t","--thread",default=50,type=int,help="Threads")
    return parser


def ping(host):
    system = platform.system().lower()
    if system == "windows":
        command = ["ping","-n","1","-w","1000",host]
    else:
        command = ["ping","-c","1","-w","1000",host]
    try:
        result = subprocess.run(
            command,
            stdout= subprocess.DEVNULL,
            stderr= subprocess.DEVNULL,
            timeout= 2
        )
        return result.returncode == 0
    except(
        subprocess.TimeoutExpired,
        OSError
    ):
        return False

def build_host(network):
    base, prefix = network.split("/",1)
    prefix = int(prefix)
    if prefix != 24:
        raise ValueError("This beginner version expects a /24 network")
    parts = base.split(".")
    if len(parts) != 4:
        raise ValueError("Invalid IPv4 address")
    hosts = []
    for number in range(1,255):
        host = (
        f"{parts[0]}."
        f"{parts[1]}."
        f"{parts[2]}."
        f"{number}"
        )
        hosts.append(host)
    return hosts
            
def main():
    parser = Helpmenu()
    args = parser.parse_args()
    try:
        hosts = build_host(args.network)
    except ValueError as error:
        parser.error(str(error))
    print(f"[-] Scanning {len(hosts)} host")

    with ThreadPoolExecutor(
        max_workers=args.thread
    ) as executor:
        futures = {
            executor.submit(
                ping,
                host
            ):host
            for host in hosts
        }
        for future in as_completed(futures):
            host = futures[future]
            if future.result():
                print(f"[+] Host is up {host}")

if __name__ == "__main__":
    main()
