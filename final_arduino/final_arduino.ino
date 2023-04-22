#include <Keypad.h>
#include <Servo.h>

#define ROW_NUM    4  // four rows
#define COLUMN_NUM 4  // four columns
#define SERVO_PIN  A0 // the Arduino pin, which connects to the servo motor
#define RED_BULB   12  // the Arduino pin, which connects to the red bulb
#define YELLOW_BULB 11  // the Arduino pin, which connects to the yellow bulb
#define GREEN_BULB  13 // the Arduino pin, which connects to the blue bulb


Servo servo; // servo motor

char keys[ROW_NUM][COLUMN_NUM] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte pin_rows[ROW_NUM] = {9, 8, 7, 6}; //connect to the row pinouts of the keypad
byte pin_column[COLUMN_NUM] = {5, 4, 3, 2}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad( makeKeymap(keys), pin_rows, pin_column, ROW_NUM, COLUMN_NUM );

String x;       //Input from python program
int angle = 0; // the current angle of servo motor
unsigned long lastTime;    //Timestamp of stage 1 PIN unlock
unsigned long lastTime1;   //Timestamp of stage 2 face unlock

//Flags for locks
bool stage1=false;
bool stage2=false;

const int buzzer = A1;

void setup() {
  Serial.begin(9600);

  servo.attach(SERVO_PIN);
  servo.write(0); // Inital motor angle set to 0°
  lastTime = millis();
  lastTime1 = millis();
  //Setting pins for bulbs
  pinMode ( YELLOW_BULB, OUTPUT);    
  pinMode ( RED_BULB, OUTPUT);  
  pinMode ( GREEN_BULB, OUTPUT);  
  digitalWrite (RED_BULB, HIGH);  //Turned on the locked bulb the default   
  pinMode(buzzer, OUTPUT); //bUZZER
}

void loop() {
  char key = keypad.getKey();
  if (key) {   //If keypad button is pressed
    //Serial.print("Key Pressed: ");
    tone(buzzer, 3000); // Send 1KHz sound signal...
    delay(150);        // ...for 1 sec
    noTone(buzzer);     // Stop sound... 
    if(key=='C'&&stage2==true){
      angle = 0;
      servo.write(angle);
      digitalWrite (YELLOW_BULB, LOW);   
      digitalWrite (RED_BULB, HIGH); 
      digitalWrite (GREEN_BULB, LOW);   
      stage1=false;
      stage2=false;
      Serial.println("Rotating Servo Motor to 0°");
    }
    else 
      Serial.print(key);
  }
  if(stage1 ==true &&stage2==false&& (millis() - lastTime) > 15000){   //Shut face unlock mechanism if face not recognized within 10secs
    stage1=false;
    digitalWrite (YELLOW_BULB, LOW);   
    digitalWrite (RED_BULB, HIGH);   
    digitalWrite (GREEN_BULB, LOW);   
  }
  else if (stage2==true && (millis() - lastTime1) > 50000) { // Relock the latch after 5 secs of being unlocked
    angle = 0;
    servo.write(angle);
    digitalWrite (YELLOW_BULB, LOW);   
    digitalWrite (RED_BULB, HIGH); 
    digitalWrite (GREEN_BULB, LOW);   
    stage1=false;
    stage2=false;
    Serial.println("Rotating Servo Motor to 0°");
  }

  if(Serial.available()){  //If python code passed input to arduino
    x = Serial.readString();
    // if(x=="written"){
    //   tone(buzzer, 3000); // Send 1KHz sound signal...
    //   delay(150);        // ...for 1 sec
    //   noTone(buzzer);     // Stop sound... 
    // }
    // if(x=="closeit"&&stage2==true){
    //   angle = 0;
    //   servo.write(angle);
    //   digitalWrite (YELLOW_BULB, LOW);   
    //   digitalWrite (RED_BULB, HIGH); 
    //   digitalWrite (GREEN_BULB, LOW);   
    //   stage1=false;
    //   stage2=false;
    //   Serial.println("Rotating Servo Motor to 0°");
    // }
    if(x=="wrong"){
      tone(buzzer, 1000); // Send 1KHz sound signal...
      delay(200);        // ...for 1 sec
      noTone(buzzer);     // Stop sound...     
      delay(200); 
      tone(buzzer, 1000); // Send 1KHz sound signal...
      delay(200);        // ...for 1 sec
      noTone(buzzer);     // Stop sound...  
    }
    if(x=="enough"){
      tone(buzzer, 300); // Send 1KHz sound signal...
      delay(10000);        // ...for 1 sec
      noTone(buzzer);     // Stop sound...
    }
    if(x=="part1"){           //Stage 1 unlock
          stage1=true;
          lastTime = millis();
          digitalWrite (YELLOW_BULB, HIGH);   
          digitalWrite (RED_BULB, LOW);   
          digitalWrite (GREEN_BULB, LOW);   
    }
    else if(x=="part2"&&stage1==true){  //Stage 2 unlock
          angle = 90;
          stage2=true;
          digitalWrite (YELLOW_BULB, LOW);   
          digitalWrite (RED_BULB, LOW); 
          digitalWrite (GREEN_BULB, HIGH);  
          servo.write(angle);
          lastTime1 = millis();
          tone(buzzer, 4000); // Send 1KHz sound signal...
          delay(400);        // ...for 1 sec
          noTone(buzzer);     // Stop sound...
          //delay(1000);        // ...for 1sec
           
    }
  }
}
