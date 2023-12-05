#include <MFRC522.h>
#include <SPI.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop() {
  if (digitalRead(BOTON_LEER_TARJETA) == HIGH) {
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
      String tarjetaID = "";
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        tarjetaID += String(mfrc522.uid.uidByte[i], HEX);
      }
      Serial.println(tarjetaID);
      delay(1000); // Puedes ajustar este valor según sea necesario
    }
  }
}
