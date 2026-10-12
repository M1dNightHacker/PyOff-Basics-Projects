#!/usr/bin/python3

def banner():
    banner = """

███████╗   ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██╔════╝   ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
███████╗   ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
╚════██║   ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
███████║██╗███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚══════╝╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                        (Created by: M.Bilal Siddiqui)                                                    
"""
    print(banner)

banner()

import argparse,socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def Helpmenu():
    parser = argparse.ArgumentParser(
        description="Simple TCP port scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-H", "--host", required=True, help="Enter IP hostname or addr")
    parser.add_argument("-T", "--thread", type=int, default=50, help="Set the number of thread")
    parser.add_argument("-P", "--port",default="1-1024", help="set the port number, Use like this -P 1-1024")
    parser.add_argument("-To", "--timeout", type=float, default=1, help="set the conection time out in sec")

    return parser

parser = Helpmenu()
args = parser.parse_args()

def parse_port(value):
    ports = set()
    for part in value.split(","):
        part = part.strip()

        if "-" in part:
            start,end = part.split("-",1)
            ports.update(
                range(
                    int(start),
                    int(end)+1
                )
            )
        else:
            ports.add(int.part())

    return sorted(
        port
        for port in ports
        if 1 <= port <=65535
    )

def scan_port(host,port,timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host,port))
        if result == 0:
            return port
    except (socket.timeout, OSError):
        return None
    finally:
        sock.close()
    return None

def main():
    parser = Helpmenu()
    args = parser.parse_args()

    try:
        ports = parse_port(args.port)
    except ValueError:
        parser.error("Invalid input")

    print(f"Scanning {args.host}...")
    print(f"Scanning {len(ports)} ports...")

    open_ports = []

    with ThreadPoolExecutor(
        max_workers= args.thread
    ) as executor:
        future = {
            executor.submit(
                scan_port,
                args.host,
                port,
                args.timeout
            ) : port
            for port in ports
        }
        for future in as_completed(future):
            port = future.result()
            if port is not None:
                open_ports.append(port)

                print(f"{port} /tcp open")
    print(f"Total number of open ports: {len(open_ports)}")
if __name__ == "__main__":
    main()
