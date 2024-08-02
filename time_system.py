# time_system.py
import datetime
import time

class TimeSystem:
    def __init__(self):
        self.start_time = time.time()
        self.time_speed = 1  # 1 second in real time = 1 second in game time

    def get_current_time(self):
        elapsed_time = (time.time() - self.start_time) * self.time_speed
        return datetime.datetime.now()

    def get_formatted_time(self):
        current_time = self.get_current_time()
        return current_time.strftime("%Y-%m-%d %H:%M:%S")