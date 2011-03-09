#define LED_PIN 10
#define ANALOG_PIN 0
#define THRESHOLD 500
#define TIMER_TCCR2A 0x03
#define TIMER_TCCR2B 0x0C
#define TIMER_OCR2A 249

boolean ainStreamEnable = false;

void setup() {

    Serial.begin(115200);
    pinMode(LED_PIN,OUTPUT);

    // Initialize timer 2 - used for stimulus pulse timing
    TCCR2A = TIMER_TCCR2A;
    TCCR2B = TIMER_TCCR2B;
    OCR2A = TIMER_OCR2A;
    // Timer 2 overflow interrupt enable 
    TIMSK2 |= (1<<TOIE2) | (0<<OCIE2A);
    TCNT2 = 0;
}

void loop() {
    while (Serial.available() > 0) {
        char byte = Serial.read();
        switch (byte) {
            case 'E':
                ainStreamEnable = true;
                break;

            case 'D':
                ainStreamEnable = false; 
                break;

            default:
                break;
        }
    }
}

ISR(TIMER2_OVF_vect) {
    int sensorVal; 
    sensorVal = analogRead(ANALOG_PIN);
    if (sensorVal < THRESHOLD) {
        digitalWrite(LED_PIN,HIGH);
    }
    else {
        digitalWrite(LED_PIN,LOW);
    } 
    if (ainStreamEnable == true) {
        Serial.println(sensorVal,DEC);
    }
}
