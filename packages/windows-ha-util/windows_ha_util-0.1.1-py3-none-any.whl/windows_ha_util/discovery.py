import socket # for connecting
import requests

def is_port_open(host, port):
    """
    determine whether `host` has the `port` open
    """
    # creates a new socket
    s = socket.socket()
    try:
        # tries to connect to host using that port
        s.settimeout(0.2)

        s.connect((host, port))
        # make timeout if you want it a little faster ( less accuracy )
    except:
        # cannot connect, port is closed
        # return false
        return False
    else:
        # the connection was established, port is open!
        return True

def discover() -> []: 
    hosts = []
    for host in range(0,255): 
        print(host)
        host_ip = f"192.168.1.{host}"
        if is_port_open(host_ip, 3040):
            id = requests.get(f"http://{host_ip}:3040/api/id").json()['id']
            hosts.append({"ip": host_ip, "id": id})
    return hosts

if __name__ == "__main__":
    discover()
print("done")