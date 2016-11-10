#define MOTORL_F 6
#define MOTORL_B 5
#define MOTORR_F 10
#define MOTORR_B 11


char incomingChar = 'F';   // for incoming serial data
int speed_mult = 28;
int normalized_speed = 9;
int total_speed = normalized_speed * speed_mult;


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
            normalized_speed = incomingChar - '0';
            total_speed = normalized_speed * speed_mult;
        }
        else if (incomingChar == 'F') {
            analogWrite(MOTORL_F, total_speed);
            analogWrite(MOTORL_B, 0);
            analogWrite(MOTORR_F, total_speed);
            analogWrite(MOTORR_B, 0);
        }
        else if (incomingChar == 'B') {
            analogWrite(MOTORL_F, 0);
            analogWrite(MOTORL_B, total_speed);
            analogWrite(MOTORR_F, 0);
            analogWrite(MOTORR_B, total_speed);
        }
        else if (incomingChar == 'r') {
            analogWrite(MOTORL_F, total_speed);
            analogWrite(MOTORL_B, 0);
            analogWrite(MOTORR_F, 0);
            analogWrite(MOTORR_B, 0);
        }
        else if (incomingChar == 'R') {
            analogWrite(MOTORL_F, total_speed);
            analogWrite(MOTORL_B, 0);
            analogWrite(MOTORR_F, 0);
            analogWrite(MOTORR_B, total_speed);
        }
        else if (incomingChar == 'l') {
            analogWrite(MOTORL_F, 0);
            analogWrite(MOTORL_B, 0);
            analogWrite(MOTORR_F, total_speed);
            analogWrite(MOTORR_B, 0);
        }
        else if (incomingChar == 'L') {
            analogWrite(MOTORL_F, 0);
            analogWrite(MOTORL_B, total_speed);
            analogWrite(MOTORR_F, total_speed);
            analogWrite(MOTORR_B, 0);
        }
        else {
            analogWrite(MOTORL_F, 0);
            analogWrite(MOTORL_B, 0);
            analogWrite(MOTORR_F, 0);
            analogWrite(MOTORR_B, 0);
        }

        Serial.write(incomingChar);
        // Serial.print("I received: ");
        // Serial.println(incomingChar);
    }
}
