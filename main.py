import sys
import datetime
from db import SessionLocal, Tag

class TagReceptionHandler:
    def __init__(self):
        self.last_counts = {}
        self.last_timestamps = {}
        
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

if __name__ == "__main__":
    handler = TagReceptionHandler()
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            handler.process_tag_data(line)
    except KeyboardInterrupt:
        print("\nReception handler stopped")
