import requests

class Controller:
    def __init__(self, host):
        self.host = host

    def turn_monitor_off(self): 
        requests.get(f"http://{self.host}:3040/api/monitor_off")

if __name__ == "__main__":
    controller = Controller("192.168.1.29")
    controller.turn_monitor_off()