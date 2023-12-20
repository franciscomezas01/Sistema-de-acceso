#include <MFRC522.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);

#define PIN_LCD 4
#define PUERTO_SERIAL Serial

LiquidCrystal_I2C lcd(0x27, 16, 2); 

#define SALIDA_DIGITAL 3 // Puerto donde está conectado el relé

void setup() {
  Serial.begin(9600);
  PUERTO_SERIAL.begin(9600);

  SPI.begin();
  mfrc522.PCD_Init();

  pinMode(SALIDA_DIGITAL, OUTPUT);

  lcd.begin(16, 2);
}

void loop() {
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String tarjetaID = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      tarjetaID += String(mfrc522.uid.uidByte[i], HEX);
    }
    Serial.println(tarjetaID);

    // Verificar si hay mensaje en el puerto serial
    if (PUERTO_SERIAL.available() > 0) {
      String mensaje = PUERTO_SERIAL.readStringUntil('\n');
      mensaje.trim();


      if (mensaje.equals("0")) {
        lcd.clear();
        lcd.print("Debe abonar cuota");
        digitalWrite(SALIDA_DIGITAL, LOW); 
      } else if (mensaje.equals("1")) {
        lcd.clear();
        lcd.print("Bienvenido");
        digitalWrite(SALIDA_DIGITAL, HIGH); 
        delay(2000); 
        lcd.clear();
        digitalWrite(SALIDA_DIGITAL, LOW); 
      }
    }

    delay(1000); 
    lcd.clear();
  }
}
