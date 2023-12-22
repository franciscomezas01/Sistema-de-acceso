#include <Wire.h>
#include <LCD.h>
#include <LiquidCrystal_I2C.h>

//esta primera version imprime un id de tarjeta constantemente 
LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7); // DIR, E, RW, RS, D4, D5, D6, D7

void setup() {
  Serial.begin(9600);
  lcd.setBacklightPin(3, POSITIVE);
  lcd.setBacklight(HIGH);
  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);

}

void loop() {
        lcd.setCursor(0, 0);
      lcd.print("GYM");
      Serial.println("46329841");
  if (Serial.available() > 0) {
    // Leer el número enviado por Python
    int numero_recibido = Serial.parseInt();

    if (numero_recibido == 0) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Paga la cuota rata");
      delay(3000);
      lcd.clear();
    } else if (numero_recibido == 1) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("BIENVENIDO");
      delay(3000);
      lcd.clear();
    } else if (numero_recibido == 2) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Ha excedido la cantidad de entradas permitidas para esta semana");
      delay(3000);
      lcd.clear();
    } else if (numero_recibido == 4) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("no existe este usuario");
      delay(3000);
      lcd.clear();
    }
  }

}

