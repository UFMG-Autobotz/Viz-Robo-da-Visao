#define MAX_BUFF_LEN        255 
#define CMD_BUFF_LEN        6

// Satates of the LED   
#define FOWARD_STATE             1      
#define BACK_STATE               2       
#define RIGHT_STATE              3      
#define LEFT_STATE               4       
#define STOP_STATE               5

// Motor A
int motor1Pin1 = 27;
int motor1Pin2 = 26;
int enable1Pin = 14;

//Motor B
int motor2Pin1 = 32;
int motor2Pin2 = 33;
int enable2Pin = 25;

// Setting PWM properties
const int freq = 5000;  
const int pwmChannel = 0;
const int resolution = 8;
int dutyCycle = 128;


#define DEFAULT_DELAY       1000

// Globals
char c; // IN char
char str[CMD_BUFF_LEN];
uint8_t idx = 0; // Reading index

uint8_t state = FOWARD_STATE; // Default state
int delay_t = DEFAULT_DELAY; // Default blinking delay
unsigned long prev_time;


// Func prototypes
uint8_t interpret(char);


void setup() {
  // Config serial port
  Serial.begin(115200);

  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(enable2Pin, OUTPUT);

  // configure LED PWM functionalitites
  ledcSetup(pwmChannel, freq, resolution);

  // attach the channel to the GPIO to be controlled
  ledcAttachPin(enable1Pin, pwmChannel);
  ledcAttachPin(enable2Pin, pwmChannel);

  // 
  prev_time = millis();
}

void loop() {

  ledcWrite(pwmChannel, dutyCycle);
  
  // Parse incoming command
  if(Serial.available() > 0){ // There's a command
    
    c = Serial.read(); // Read one byte
    
    if(c != '\n'){ // Still reading
      str[idx++] = c; // Parse the string byte (char) by byte
    }
    else{ // Done reading
      str[idx] = '\0'; // Convert it to a string
      
      // Determine nature of the command
      state = interpret(str[0]);

      // Setting de idx to the begin
      idx = 0;
    }
  }
  else{ // No input from commander
    state = 0;
  }

  // Main state machine
  switch(state){
    case FOWARD_STATE:
      Serial.println("Moving Foward");
      digitalWrite(motor1Pin1, HIGH);
      digitalWrite(motor1Pin2, LOW);
      digitalWrite(motor2Pin1, HIGH);
      digitalWrite(motor2Pin2, LOW);
      break;
      
    case BACK_STATE:
      Serial.println("Moving Backwards");
      digitalWrite(motor1Pin1, LOW);
      digitalWrite(motor1Pin2, HIGH);
      digitalWrite(motor2Pin1, LOW);
      digitalWrite(motor2Pin2, HIGH);
      break;
    
    case RIGHT_STATE:
      Serial.println("Moving Right");
      digitalWrite(motor1Pin1, LOW);
      digitalWrite(motor1Pin2, HIGH);
      digitalWrite(motor2Pin1, HIGH);
      digitalWrite(motor2Pin2, LOW);
      break;
    
    case LEFT_STATE:
      Serial.println("Moving Left");
      digitalWrite(motor1Pin1, HIGH);
      digitalWrite(motor1Pin2, LOW);
      digitalWrite(motor2Pin1, LOW);
      digitalWrite(motor2Pin2, HIGH);
      break;
    
    case STOP_STATE:
      Serial.println("Stopping");
      digitalWrite(motor1Pin1, LOW);
      digitalWrite(motor1Pin2, LOW);
      digitalWrite(motor2Pin1, LOW);
      digitalWrite(motor2Pin2, LOW);
      break;
  }
  
}

// Func definition

uint8_t interpret(char c){
  switch(c){
    case 'w': return FOWARD_STATE;

    case 's': return BACK_STATE;

    case 'd': return RIGHT_STATE;

    case 'a': return LEFT_STATE;

    case 'q': return STOP_STATE;

    default: Serial.println("UNKNOWN");
  }
  return state; // Don't change anything
}




























