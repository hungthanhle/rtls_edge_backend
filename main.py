import socket
import datetime
from db import SessionLocal, Tag

class TagReceptionHandler:
    def __init__(self):
        self.last_counts = {}
        self.last_timestamps = {}
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect_to_simulator(self):
        try:
            self.client_socket.connect(('localhost', 5000))
            print("Connected to tag simulator server")
            return True
        except ConnectionRefusedError:
            print("Cannot connect to simulator. Is it running?")
            return False
        
    def process_tag_data(self, line):
        try:
            # Parse the tag data
            parts = line.strip().split(',')
            if len(parts) != 4 or parts[0] != "TAG":
                return
            
            tag_id = parts[1]
            count = int(parts[2])
            timestamp_str = parts[3]
            
            # Convert timestamp string to datetime
            timestamp = datetime.datetime.strptime(timestamp_str, "%Y%m%d%H%M%S.%f")
            
            # Check if count changed
            if tag_id in self.last_counts and count != self.last_counts[tag_id]:
                print(f"Count changed for {tag_id}: {self.last_counts[tag_id]} -> {count}")
            
            # Update last known values
            self.last_counts[tag_id] = count
            self.last_timestamps[tag_id] = timestamp
            
            # Update tag in database
            db = SessionLocal()
            tag = db.query(Tag).filter(Tag.tag_id == tag_id).first()
            if tag:
                tag.last_cnt = count
                tag.last_seen = timestamp
                db.commit()
            db.close()
            
        except Exception as e:
            print(f"Error processing line: {e}")

    def start_receiving(self):
        try:
            while True:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                for line in data.splitlines():
                    self.process_tag_data(line)
                    
        except KeyboardInterrupt:
            print("\nReception handler stopped")
        finally:
            self.client_socket.close()

if __name__ == "__main__":
    handler = TagReceptionHandler()
    if handler.connect_to_simulator():
        handler.start_receiving()
