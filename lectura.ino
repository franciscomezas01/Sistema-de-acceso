#include <MFRC522.h>
#include <SPI.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);

#define BOTON_LEER_TARJETA 2
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
