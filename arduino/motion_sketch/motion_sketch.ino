#define MOTORL_F 6
#define MOTORL_B 5
#define MOTORR_F 10
#define MOTORR_B 11


char actionChar = 'S';   // global action state
char incomingChar;
int normalized_speed = 9; // Speed input, always an int in [0, 9]
int speed_mult = 28;  // 28 b/c 9*[0, 9] = [0, 252] in [0, 255]
int total_speed = normalized_speed * speed_mult;  // global speed state


void setup() {
    // put your setup code here, to run once:
    pinMode(MOTORL_F, OUTPUT);
    pinMode(MOTORL_B, OUTPUT);
    pinMode(MOTORR_F, OUTPUT);
    pinMode(MOTORR_B, OUTPUT);
    
    Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
}

void loop() {
    // put your main code here, to run repeatedly:
    
    // send data only when you receive data:
    if (Serial.available() > 0) {
        // read the incoming byte:
        incomingChar = Serial.read();

        if (incomingChar >= '0' and incomingChar <= '9') {
            // set speed
            normalized_speed = incomingChar - '0';
            total_speed = normalized_speed * speed_mult;
        }
        else {
            // set action
            actionChar = incomingChar;
        }

        // write back the command for testing purposes
        Serial.write(incomingChar);
    }

    
    if (actionChar == 'F') {  // Forward
        analogWrite(MOTORL_F, total_speed);
        analogWrite(MOTORL_B, 0);
        analogWrite(MOTORR_F, total_speed);
        analogWrite(MOTORR_B, 0);
    }
    else if (actionChar == 'B') { // Backward
        analogWrite(MOTORL_F, 0);
        analogWrite(MOTORL_B, total_speed);
        analogWrite(MOTORR_F, 0);
        analogWrite(MOTORR_B, total_speed);
    }
    else if (actionChar == 'r') { // right
        analogWrite(MOTORL_F, total_speed);
        analogWrite(MOTORL_B, 0);
        analogWrite(MOTORR_F, 0);
        analogWrite(MOTORR_B, 0);
    }
    else if (actionChar == 'R') { // hard right
        analogWrite(MOTORL_F, total_speed);
        analogWrite(MOTORL_B, 0);
        analogWrite(MOTORR_F, 0);
        analogWrite(MOTORR_B, total_speed);
    }
    else if (actionChar == 'l') { // left
        analogWrite(MOTORL_F, 0);
        analogWrite(MOTORL_B, 0);
        analogWrite(MOTORR_F, total_speed);
        analogWrite(MOTORR_B, 0);
    }
    else if (actionChar == 'L') { // hard left
        analogWrite(MOTORL_F, 0);
        analogWrite(MOTORL_B, total_speed);
        analogWrite(MOTORR_F, total_speed);
        analogWrite(MOTORR_B, 0);
    }
    else {  // Everything else is stop (preferably 'S')
        analogWrite(MOTORL_F, 0);
        analogWrite(MOTORL_B, 0);
        analogWrite(MOTORR_F, 0);
        analogWrite(MOTORR_B, 0);
    }
}
