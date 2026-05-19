import psutil

    def collect_network():

        network_data = []

        connections = psutil.net_connections()

        for conn in connections:

            try:

                if conn.raddr:

                    network_info = {
                        "local_ip": conn.laddr.ip,
                        "local_port": conn.laddr.port,
                        "remote_ip": conn.raddr.ip,
                        "remote_port": conn.raddr.port,
                        "status": conn.status,
                        "pid": conn.pid
                    }

                    network_data.append(network_info)

            except:

                continue

        return network_data