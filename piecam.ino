// C++ code
//
int buzzer_pin = 8;
int pir_pin = 9;

void setup()
{
  pinMode(buzzer_pin, OUTPUT);
  pinMode(pir_pin, INPUT);
  Serial.begin(9600); 
}

void loop()
{
  if(digitalRead(pir_pin) == HIGH)
  {
    Serial.println("1");
    digitalWrite(buzzer_pin, 1);
    delay(250); // Wait for 1000 millisecond(s)
    digitalWrite(buzzer_pin, 0);
    delay(250);
  }
  else
  {
    Serial.println("0");
    digitalWrite(buzzer_pin, 0);
    delay(250);
  }
}
