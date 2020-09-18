// Test of full software-defined PWM for RGB LEDs
#define ON true
#define OFF false

unsigned long currentMicros = micros();
unsigned long previousMicros = 0;
unsigned long microInterval = 40;

const int pwmMax = 255;
int tickCount = 0;

typedef struct cube {
  int pinR;
  int pinG;
  int pinB;

  int pwmR;
  int pwmG;
  int pwmB;

  bool stateR;
  bool stateG;
  bool stateB;
} cube;

const int cubeCount = 1;
cube cubes[cubeCount];

void setupPWM() {
  cubes[0].pinR = 2;
  cubes[0].pinG = 3;
  cubes[0].pinB = 4;

  cubes[0].pwmR = 0;
  cubes[0].pwmG = 0;
  cubes[0].pwmB = 0;

  cubes[0].stateR = ON;
  cubes[0].stateG = ON;
  cubes[0].stateB = ON;

  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
}

void handlePWM() {
  currentMicros = micros();
  if (currentMicros - previousMicros >= microInterval) {
    tickCount++;

    if (cubes[0].stateR == ON) {
      if (tickCount >= cubes[0].pwmR) {
        cubes[0].stateR = OFF;
      }
    } else {
      if (tickCount >= pwmMax) {
        cubes[0].stateR = OFF;
      }
    }

    if (cubes[0].stateG == ON) {
      if (tickCount >= cubes[0].pwmG) {
        cubes[0].stateG = OFF;
      }
    } else {
      if (tickCount >= pwmMax) {
        cubes[0].stateG = OFF;
      }
    }

    if (cubes[0].stateB == ON) {
      if (tickCount >= cubes[0].pwmB) {
        cubes[0].stateB = OFF;
      }
    } else {
      if (tickCount >= pwmMax) {
        cubes[0].stateB = OFF;
      }
    }

    if (tickCount >= pwmMax) {
      tickCount = 0;
      if (cubes[0].pwmR > 0) {
        cubes[0].stateR = ON;
      } if (cubes[0].pwmG > 0) {
        cubes[0].stateG = ON;
      } if (cubes[0].pwmB > 0) {
        cubes[0].stateB = ON;
      }
    }

    digitalWrite(cubes[0].pinR, cubes[0].stateR);
    digitalWrite(cubes[0].pinG, cubes[0].stateG);
    digitalWrite(cubes[0].pinB, cubes[0].stateB);

    previousMicros = currentMicros;
  }
}

void rainbowFade() {//TODO
    // initially, we intended to add some dynamic lighting functions directly on the controllers
    // this turned out to be more of a pain than it was worth, and the Arduino code was kept simple
}

void strobe() {//TODO
    // same as above
}

void setup() {
  setupPWM();
}

void loop() {
  handlePWM();
}
