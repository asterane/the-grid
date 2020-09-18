/* Full software-defined PWM for RGB LEDs
 * Controlled over serial connection
 *  By Matthew Rothlisberger
 *  2019
 */

// these specify macros for easier reading
#define ON true
#define OFF false

// tracks microseconds since program start
unsigned long currentMicros = micros();

// saves time of last PWM check completion
unsigned long previousMicros = 0;

// used to hold the difference between cur. and prev. time
unsigned long diffMicros = 0;

// ideal number of microseconds between PWM checks
unsigned long microInterval = 40;

// maximum PWM value, and tracker for checks
const byte pwmMax = 255;
int tickCount = 0;
bool cycleEnd = false;

// variables for serial communication
const char packetStart = '?';
char packet[2];

// attributes of every intensity channel
typedef struct chan {
  byte pin;
  byte pwm;
  bool state;
} chan;

// initalizes channel array
const byte chanCount = 48;
chan channels[chanCount];

// begins serial connection and sends number of controllable channels
void setupSerial() {
  Serial.begin(115200);
  while (!Serial) { ; }
  Serial.write(chanCount);
}

// checks for new data packets every cycle and changes intensities
void handleSerial() {
  while ( (cycleEnd) && (Serial.read() == packetStart) ) {
    Serial.readBytes(packet, 2);
    channels[packet[0]-1].pwm = packet[1];
    //Serial.write(channels[packet[0]-1].pwm);
  }

  cycleEnd = false;
}

// sets up initial values for every intensity channel
void setupPWM() {
  for (int i=0;i<chanCount;i++) {
    channels[i].pin = i+2;
    channels[i].pwm = 0;
    channels[i].state = ON;

    pinMode(i, OUTPUT);
    digitalWrite(channels[i].pin, channels[i].state);
  }
}

// performs PWM checks at appropriate intervals
void handlePWM() {
  currentMicros = micros();

  // resets time counter after rollover at ~70 minutes
  if (currentMicros < previousMicros) {
    previousMicros = 0;
  }

  diffMicros = currentMicros - previousMicros;

  // only check if enough time has passed since the last one
  if (diffMicros >= microInterval) {

    // this bit really speeds things up
    tickCount += (diffMicros / microInterval);
    //Serial.write(tickCount);

    // restart the PWM cycle after 255 ticks
    if (tickCount >= pwmMax) {
      tickCount = 0;
      cycleEnd = true;

      for (int i=0;i<chanCount;i++) {
        if (channels[i].pwm > 0) {
          channels[i].state = ON;
          portWrite(channels[i].pin, channels[i].state);
        }
      }
    }

    // check every channel; turn off until next cycle if necessary
    else {
      for (int i=0;i<chanCount;i++) {
        if ( (channels[i].state) && (tickCount >= channels[i].pwm) ) {
          channels[i].state = OFF;
          portWrite(channels[i].pin, channels[i].state);
        }
      }
    }

    previousMicros = currentMicros;
  }
}

// acts as faster digitalWrite to save CPU cycles
void portWrite(byte pin, bool state) {
  if (state == true) {
    switch (pin) {
      case 0: PORTE |= 0b00000001; break;
      case 1: PORTE |= 0b00000010; break;
      case 2: PORTE |= 0b00010000; break;
      case 3: PORTE |= 0b00100000; break;
      case 4: PORTG |= 0b00100000; break;
      case 5: PORTE |= 0b00001000; break;
      case 6: PORTH |= 0b00001000; break;
      case 7: PORTH |= 0b00010000; break;
      case 8: PORTH |= 0b00100000; break;
      case 9: PORTH |= 0b01000000; break;
      case 10: PORTB |= 0b00010000; break;
      case 11: PORTB |= 0b00100000; break;
      case 12: PORTB |= 0b01000000; break;
      case 13: PORTB |= 0b10000000; break;
      case 14: PORTJ |= 0b00000010; break;
      case 15: PORTJ |= 0b00000001; break;
      case 16: PORTH |= 0b00000010; break;
      case 17: PORTH |= 0b00000001; break;
      case 18: PORTD |= 0b00001000; break;
      case 19: PORTD |= 0b00000100; break;
      case 20: PORTD |= 0b00000010; break;
      case 21: PORTD |= 0b00000001; break;
      case 22: PORTA |= 0b00000001; break;
      case 23: PORTA |= 0b00000010; break;
      case 24: PORTA |= 0b00000100; break;
      case 25: PORTA |= 0b00001000; break;
      case 26: PORTA |= 0b00010000; break;
      case 27: PORTA |= 0b00100000; break;
      case 28: PORTA |= 0b01000000; break;
      case 29: PORTA |= 0b10000000; break;
      case 30: PORTC |= 0b10000000; break;
      case 31: PORTC |= 0b01000000; break;
      case 32: PORTC |= 0b00100000; break;
      case 33: PORTC |= 0b00010000; break;
      case 34: PORTC |= 0b00001000; break;
      case 35: PORTC |= 0b00000100; break;
      case 36: PORTC |= 0b00000010; break;
      case 37: PORTC |= 0b00000001; break;
      case 38: PORTD |= 0b10000000; break;
      case 39: PORTG |= 0b00000100; break;
      case 40: PORTG |= 0b00000010; break;
      case 41: PORTG |= 0b00000001; break;
      case 42: PORTL |= 0b10000000; break;
      case 43: PORTL |= 0b01000000; break;
      case 44: PORTL |= 0b00100000; break;
      case 45: PORTL |= 0b00010000; break;
      case 46: PORTL |= 0b00001000; break;
      case 47: PORTL |= 0b00000100; break;
      case 48: PORTL |= 0b00000010; break;
      case 49: PORTL |= 0b00000001; break;
      case 50: PORTB |= 0b00001000; break;
      case 51: PORTB |= 0b00000100; break;
      case 52: PORTB |= 0b00000010; break;
      case 53: PORTB |= 0b00000001; break;
    }
  } else {
    switch (pin) {
      case 0: PORTE &= 0b11111110; break;
      case 1: PORTE &= 0b11111101; break;
      case 2: PORTE &= 0b11101111; break;
      case 3: PORTE &= 0b11011111; break;
      case 4: PORTG &= 0b11011111; break;
      case 5: PORTE &= 0b11110111; break;
      case 6: PORTH &= 0b11110111; break;
      case 7: PORTH &= 0b11101111; break;
      case 8: PORTH &= 0b11011111; break;
      case 9: PORTH &= 0b10111111; break;
      case 10: PORTB &= 0b11101111; break;
      case 11: PORTB &= 0b11011111; break;
      case 12: PORTB &= 0b10111111; break;
      case 13: PORTB &= 0b01111111; break;
      case 14: PORTJ &= 0b11111101; break;
      case 15: PORTJ &= 0b11111110; break;
      case 16: PORTH &= 0b11111101; break;
      case 17: PORTH &= 0b11111110; break;
      case 18: PORTD &= 0b11110111; break;
      case 19: PORTD &= 0b11111011; break;
      case 20: PORTD &= 0b11111101; break;
      case 21: PORTD &= 0b11111110; break;
      case 22: PORTA &= 0b11111110; break;
      case 23: PORTA &= 0b11111101; break;
      case 24: PORTA &= 0b11111011; break;
      case 25: PORTA &= 0b11110111; break;
      case 26: PORTA &= 0b11101111; break;
      case 27: PORTA &= 0b11011111; break;
      case 28: PORTA &= 0b10111111; break;
      case 29: PORTA &= 0b01111111; break;
      case 30: PORTC &= 0b01111111; break;
      case 31: PORTC &= 0b10111111; break;
      case 32: PORTC &= 0b11011111; break;
      case 33: PORTC &= 0b11101111; break;
      case 34: PORTC &= 0b11110111; break;
      case 35: PORTC &= 0b11111011; break;
      case 36: PORTC &= 0b11111101; break;
      case 37: PORTC &= 0b11111110; break;
      case 38: PORTD &= 0b01111111; break;
      case 39: PORTG &= 0b11111011; break;
      case 40: PORTG &= 0b11111101; break;
      case 41: PORTG &= 0b11111110; break;
      case 42: PORTL &= 0b01111111; break;
      case 43: PORTL &= 0b10111111; break;
      case 44: PORTL &= 0b11011111; break;
      case 45: PORTL &= 0b11101111; break;
      case 46: PORTL &= 0b11110111; break;
      case 47: PORTL &= 0b11111011; break;
      case 48: PORTL &= 0b11111101; break;
      case 49: PORTL &= 0b11111110; break;
      case 50: PORTB &= 0b11110111; break;
      case 51: PORTB &= 0b11111011; break;
      case 52: PORTB &= 0b11111101; break;
      case 53: PORTB &= 0b11111110; break;
    }
  }
}

/*
// turns everything on at once, not really necessary
void blanketWrite() {
  PORTA = 0b11111111;
  PORTB = 0b11111111;
  PORTC = 0b11111111;
  PORTD |= 0b10001111;
  PORTE |= 0b00111000;
  PORTG |= 0b00100111;
  PORTH |= 0b01111011;
  PORTJ |= 0b00000011;
  PORTL = 0b11111111;
}
*/

void setup() {
  setupSerial();
  setupPWM();
}

void loop() {
  handlePWM();
  handleSerial();
}
