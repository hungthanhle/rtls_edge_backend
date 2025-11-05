import time
import datetime
import sys
from random import randint

class TagSimulator:
    def __init__(self):
        self.tags = {
            "fa451f0755d8": 0,
            "fb892e1866c9": 0,
            "fc234a7944b2": 0
        }

    def generate_tag_data(self):
        while True:
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime("%Y%m%d%H%M%S.%f")[:-3]
            
            for tag_id in self.tags:
                self.tags[tag_id] += randint(1, 3)  # Increment counter randomly
                log_line = f"TAG,{tag_id},{self.tags[tag_id]},{timestamp}"
                print(log_line)
                sys.stdout.flush()
            
            time.sleep(2)  # Update every 2 seconds

if __name__ == "__main__":
    simulator = TagSimulator()
    try:
        simulator.generate_tag_data()
    except KeyboardInterrupt:
        print("\nSimulator stopped")
