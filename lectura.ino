#include <MFRC522.h>
#include <SPI.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);

#define BOTON_LEER_TARJE#include <MFRC522.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);

#define PIN_LCD 4
#define PUERTO_SERIAL Serial

LiquidCrystal_I2C lcd(0x27, 16, 2); // Dirección I2C de la LCD y dimensiones (ajusta según tu LCD)

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

      // Lógica para mostrar mensajes en la LCD y activar la salida digital
      if (mensaje.equals("0")) {
        lcd.clear();
        lcd.print("Debe abonar cuota");
        digitalWrite(SALIDA_DIGITAL, LOW); // Desactivar el relé
      } else if (mensaje.equals("1")) {
        lcd.clear();
        lcd.print("Bienvenido");
        digitalWrite(SALIDA_DIGITAL, HIGH); // Activar el relé
        delay(2000); // Mantener el mensaje durante 2 segundos
        lcd.clear();
        digitalWrite(SALIDA_DIGITAL, LOW); // Desactivar el relé después de mostrar el mensaje
      }
    }

    delay(1000); // Puedes ajustar este valor según sea necesario
    lcd.clear();
  }
}
TA 2
#define PIN_LCD 4

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  
  pinMode(BOTON_LEER_TARJETA, INPUT);
}

void loop() {
  if (digitalRead(BOTON_LEER_TARJETA) == HIGH) {
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
      String tarjetaID = "";
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        tarjetaID += String(mfrc522.uid.uidByte[i], HEX);
      }
      Serial.println(tarjetaID);

      // Lógica para permitir o denegar el acceso
      if (puedeEntrar(tarjetaID)) {
        Serial.println("Puede entrar");
        digitalWrite(PIN_LCD, HIGH); // Enciende la LCD (ajusta según tu configuración)
        delay(2000); // Muestra el mensaje durante 2 segundos
        digitalWrite(PIN_LCD, LOW); // Apaga la LCD
      } else {
        Serial.println("No puede entrar");
        // Puedes mostrar un mensaje diferente en la LCD si se deniega el acceso
      }

      delay(1000); // Puedes ajustar este valor según sea necesario
    }
  }
}

bool puedeEntrar(String tarjetaID) {
  // Agrega tu lógica para permitir o denegar el acceso según el tarjetaID
  // Puedes basarte en la lógica que ya tienes en tu programa Python
  // Devuelve true si puede entrar, false si no puede
  return true; // Cambia esto según tu lógica
}
