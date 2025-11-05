import time
import datetime
import socket
from random import randint
import threading

class TagSimulator:
    def __init__(self):
        self.tags = {
            "fa451f0755d8": 0,
            "fb892e1866c9": 0,
            "fc234a7944b2": 0
        }
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket = None
        self.running = True

    def generate_tag_data(self):
        while self.running:
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime("%Y%m%d%H%M%S.%f")[:-3]
            
            for tag_id in self.tags:
                self.tags[tag_id] += randint(1, 3)
                log_line = f"TAG,{tag_id},{self.tags[tag_id]},{timestamp}"
                print(log_line)  # Print to console
                
                # Send to client if connected
                if self.client_socket:
                    try:
                        self.client_socket.send((log_line + "\n").encode('utf-8'))
                    except Exception as e:
                        print(f"Error sending to client: {e}")
                        self.client_socket = None
            
            time.sleep(2)

    def handle_client(self, client_socket, addr):
        print(f"Reception handler connected from {addr}")
        self.client_socket = client_socket
        try:
            while self.running:
                time.sleep(1)  # Keep connection alive
        except Exception as e:
            print(f"Client disconnected: {e}")
        finally:
            self.client_socket = None
            client_socket.close()

    def start_server(self):
        self.server_socket.bind(('localhost', 5000))
        self.server_socket.listen(1)
        print("Tag simulator server started on port 5000...")
        
        # Start data generation in separate thread
        generator_thread = threading.Thread(target=self.generate_tag_data)
        generator_thread.start()
        
        try:
            while self.running:
                client_socket, addr = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, addr)
                )
                client_thread.start()
        except KeyboardInterrupt:
            print("\nSimulator server stopped")
            self.running = False
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    simulator = TagSimulator()
    simulator.start_server()
