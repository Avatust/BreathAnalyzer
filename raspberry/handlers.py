import json
import sys
from tweeter import Tweeter
from camera import Obscura
from datetime import datetime
import serial


class OnThresholdExceededHandler:

    def __init__(self,
                 output_file,
                 tweeter: Tweeter,
                 camera: Obscura,
                 serial_conn: serial.Serial,
                 status_maker=lambda datetime, value, message: 'This one at ' + str(datetime),
                 filename_generator=lambda: 'image.jpg'):
        self.file = output_file
        self.tweeter = tweeter
        self.camera = camera
        self.serial_conn = serial_conn
        self.status_maker = status_maker
        self.filename_generator = filename_generator

    def __call__(self, value, message):
        # print('on_threshold_exceeded called, value', value)
        self.print_message_on_sensor("{}\n({:.1f} units)".format(message, value))
        dt = datetime.now()
        response = self.picture_twitter_and_response(
            self.status_maker(dt, value, message))

        media_url = self.tweeter.extract_media_url(response)

        self.print_to_file(value, message, dt, media_url)

    def print_message_on_sensor(self, msg: str):
        out = ""
        for line in msg.splitlines():
            while len(line) > 21:
                out += "{:^20}-".format(line[:20])
                line=line[20:]
            out += "{:^21}".format(line)

        self.serial_conn.write(out.encode())

    def picture_twitter_and_response(self, status):
        filename = self.filename_generator()
        # print('taking picture ({})'.format(filename))
        self.camera.take_and_save_img(filename)
        # print('tweeting')
        return self.tweeter.tweet(status, filename)

    def print_to_file(self, value, message, datetime, media_url):
        # print('printing to', self.file)
        payload = {
            "timestamp": str(datetime),
            "value": value,
            "message": message,
            "picture": media_url
        }
        try:
            with open(self.file, 'a') as f:
                print(json.dumps(payload), file=f)
        except Exception as e:
            print(e, file=sys.stderr)
