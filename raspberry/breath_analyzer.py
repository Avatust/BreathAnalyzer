# from collections import deque as CircularArray
from numpy_ringbuffer import RingBuffer as CircularArray
import numpy as np

DEBUG = True
HEADER_PRINTED = False


class BreathAnalyzer:
    thresholdMessageMap = {
        0: "You're fine!",
        10: "Your breath smells...",
        20: "You've been drinking!",
        50: "Don't drive!",
        80: "You're wasted!"
    }

    raw_min = 33.0
    raw_max = 150.0
    scaling_exponent = 1.2
    slope_threshold = 5
    slope_reference_index_ratio = 0.8  # 0 for oldest, 1 for newest
    seconds_to_keep_history = 4
    std_dev_lock_limit = 0.6
    std_dev_adjust_limit = 0.2

    thresholds = sorted(thresholdMessageMap.keys(), reverse=True)
    minThreshold = thresholds[-1]

    def __init__(self, samples_per_second, on_threshold_exceeded, on_reset=None):
        arr_size = int(samples_per_second * self.seconds_to_keep_history)
        self.gasHistory = CircularArray(arr_size)
        self.slope_reference_index = int(arr_size * self.slope_reference_index_ratio)

        self.on_threshold_exceeded = on_threshold_exceeded
        self.on_reset = on_reset
        self.header_printed = False
        self.lock = True
        self.called = True

    def debug(self, input_val, max_val, std, ref, slope):
        if not DEBUG: return
        if not self.header_printed:
            self.header_printed = True
            states = (
                "Input", "Max.val.", "Std.dev.", "Ref.", "Slope", "R_min", "R_max", "Lock"
            )
            print(("{:>8}  " * len(states)).format(*states))
        args = (
            input_val, max_val, std, ref, slope, self.raw_min, self.raw_max, self.lock
        )
        print(("{: 8.3f}  " * len(args) + " " * 20).format(*args), end='\r')

    def add_gas_concentration(self, units):
        self.gasHistory.append(units)
        if self.gasHistory.is_full:
            self.check_concentration()

    def check_concentration(self):
        arr = self.gasHistory
        curr = np.mean(arr[-4:])
        ref = np.mean(arr[self.slope_reference_index:self.slope_reference_index + 4])
        slope = curr - ref
        std = np.std(arr)
        max_val = np.max(arr)

        self.debug(curr, max_val, std, ref, slope)

        if self.lock:
            if std < self.std_dev_lock_limit:
                self.reset()
            elif slope < 0 and not self.called:
                self.called = True
                self.call_handler(self.scale(max_val))

        else:
            if slope > self.slope_threshold:
                self.lock = True
            elif std < self.std_dev_adjust_limit and abs(self.raw_min - curr) > 1:
                self.raw_min = np.round(np.mean(arr))

    def scale(self, value):
        # adjust range
        if self.raw_max < value:
            self.raw_max = np.ceil(value)
        if self.raw_min > value:
            self.raw_min = np.floor(value)

        normalized = (
                (value - self.raw_min)
                / (self.raw_max - self.raw_min))

        return 100 * normalized ** self.scaling_exponent  # keep between 0 and 100

    def reset(self):
        self.lock = False
        self.called = False
        if callable(self.on_reset):
            self.on_reset()

    def call_handler(self, value):
        if callable(self.on_threshold_exceeded):
            self.on_threshold_exceeded(value, self.get_message_for_threshold(value))

    def get_message_for_threshold(self, value):
        for key in self.thresholds:
            if key <= value:
                return self.thresholdMessageMap[key]

        return ""
