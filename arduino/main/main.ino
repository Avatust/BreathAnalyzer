#include "circular_array.h"
#include "Adafruit_SSD1306.h"

#if (SSD1306_LCDHEIGHT != 64)
#error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif

const int SENSOR_PIN = 0;
const int DISP_ADDR = 0x3C;

const float SAMPLES_PER_SECOND =             20; // these are outputed to the serial interface
const int   READINGS_PER_SAMPLE =             5; // reads the sensor this many times before
                                                 // calculating value of the current sample
const int READING_ARRAY_SIZE =               30; // these many recent readings will be averaged


const int DELAY_BETWEEN_READINGS = 1000 / (SAMPLES_PER_SECOND*READINGS_PER_SAMPLE);

void printCentered(Adafruit_SSD1306 & disp, const String & str);
void sample_sensor_and_write();
void check_and_display_serial_input();

CircularArray<int, READING_ARRAY_SIZE> readings;
Adafruit_SSD1306 display(-1);

void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, DISP_ADDR);
  display.clearDisplay();
  display.setTextColor(WHITE);
  printCentered(display, String("Initializing..."));
  display.display();
  
  Serial.begin(9600);
  Serial.print("SPS=");
  Serial.println(SAMPLES_PER_SECOND);

  // fill array
  for (int i = 0; i < READING_ARRAY_SIZE; ++i)
  {
      delay(DELAY_BETWEEN_READINGS);
      readings.pushValue(analogRead(SENSOR_PIN));
  }
}

void loop() {
    sample_sensor_and_write();
    check_and_display_serial_input();
}


void sample_sensor_and_write() {
    for (int i = 0; i < READINGS_PER_SAMPLE; ++i) {
      delay(DELAY_BETWEEN_READINGS);
      readings.pushValue(analogRead(SENSOR_PIN));
    }
    Serial.println(readings.getAverage()); // MAX AT 150, base 30
}


void check_and_display_serial_input()
{
  if (Serial.available()) {
    display.clearDisplay();
    printCentered(display, Serial.readString());
    display.display();
  }
}


void printCentered(Adafruit_SSD1306 & disp, const String & str)
{
  const int WIDTH = 6, HEIGHT = 8;
  const int ROWS = 8, COLS = 21;
  
  int remaining = str.length();
  remaining = min(remaining, ROWS*COLS);
  
  int lines = ceil((float)remaining / COLS);

  int horizontal_center = (lines > 1) ? 1 : (SSD1306_LCDWIDTH  - remaining*WIDTH) / 2 + 1;
  int vertical_center = (SSD1306_LCDHEIGHT - lines*HEIGHT) / 2;

  int pos = 0, chop;
  for (int line = 0, pos = 0; line < lines; ++line)
  {
    disp.setCursor(horizontal_center, vertical_center + line*HEIGHT);
    disp.print(str.substring(pos, pos + COLS));
    pos += COLS;
  }
}
