import time
import datetime
import socket
from random import randint

class TagSimulator:
    def __init__(self):
        self.tags = {
            "fa451f0755d8": 0,
            "fb892e1866c9": 0,
            "fc234a7944b2": 0
        }
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def start_server(self):
        self.server_socket.bind(('localhost', 5000))
        self.server_socket.listen(1)
        print("Tag simulator server started on port 5000...")
        
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Reception handler connected from {addr}")
                self.generate_tag_data(client_socket)
        except KeyboardInterrupt:
            print("\nSimulator server stopped")
        finally:
            self.server_socket.close()
        
    def generate_tag_data(self, client_socket):
        try:
            while True:
                current_time = datetime.datetime.now()
                timestamp = current_time.strftime("%Y%m%d%H%M%S.%f")[:-3]
                
                for tag_id in self.tags:
                    self.tags[tag_id] += randint(1, 3)
                    log_line = f"TAG,{tag_id},{self.tags[tag_id]},{timestamp}"
                    print(log_line)  # Print to console
                    client_socket.send((log_line + "\n").encode('utf-8'))
                
                time.sleep(2)
        except Exception as e:
            print(f"Client disconnected: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    simulator = TagSimulator()
    simulator.start_server()
