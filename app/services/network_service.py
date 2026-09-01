import socket

import psutil


def get_network_metrics():
    interfaces = []

    for interface_name, addresses in psutil.net_if_addrs().items():
        interface = {
            "name": interface_name,
            "addresses": []
        }

        for address in addresses:
            interface["addresses"].append({
                "family": str(address.family),
                "address": address.address,
                "netmask": address.netmask,
                "broadcast": address.broadcast
            })

        interfaces.append(interface)

    counters = psutil.net_io_counters()

    return {
        "hostname": socket.gethostname(),
        "interfaces": interfaces,
        "traffic": {
            "bytes_sent": counters.bytes_sent,
            "bytes_received": counters.bytes_recv,
            "packets_sent": counters.packets_sent,
            "packets_received": counters.packets_recv,
            "errors_in": counters.errin,
            "errors_out": counters.errout,
            "dropped_in": counters.dropin,
            "dropped_out": counters.dropout
        }
    }