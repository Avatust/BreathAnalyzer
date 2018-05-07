#!/usr/bin/python3

import handlers
import watchdog
from breath_analyzer import BreathAnalyzer
from camera import Obscura
from tweeter import Tweeter

if __name__ == "__main__":
    with watchdog.get_connection_to_arduino() as serialConn:
        serialConn.read_until('SPS='.encode())
        samples_per_second = float(serialConn.readline())

        handler = handlers.OnThresholdExceededHandler(
            '/common/stream',
            Tweeter(),
            Obscura('/dev/video0', (640, 480)),
            serialConn,
            status_maker=lambda datetime, value, message: "{}\nThe value measured was {:.1f} units, at {}."
                .format(message, value, datetime.strftime("%X on %x"))
        )
        breathAnalyzer = BreathAnalyzer(samples_per_second, handler, on_reset=lambda: serialConn.write('Sensor is ready'.encode()))
        watchdog.keep_reading(serialConn, breathAnalyzer.add_gas_concentration)
