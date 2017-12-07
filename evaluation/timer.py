import math
import time


class Timer:
    def __init__(self):
        self.times = {}

    def start(self, key):
        self.times[key] = Timer.current_time_millis()

    def stop(self, key):
        time_elapsed = Timer.current_time_millis() - self.times[key]
        self.times[key] = time_elapsed
        return time_elapsed

    def get(self, key):
        return self.format_time(self.times[key])

    @staticmethod
    def current_time_millis():
        return int(round(time.time() * 1000))

    def format_time(self, millis):
        seconds = math.floor(millis / 1000)
        millis -= seconds * 1000
        if seconds <= 0:
            return "{0}ms".format(millis)

        minutes = math.floor(seconds / 60)
        seconds -= minutes * 60
        if minutes <= 0:
            return "{0}s {1}ms".format(seconds, millis)

        hours = math.floor(minutes / 60)
        minutes -= hours * 60
        if hours <= 0:
            return "{0}min {1}s {2}ms".format(minutes, seconds, millis)
