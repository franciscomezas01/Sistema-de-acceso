void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(0)); // Inicializar la semilla para la generación de números aleatorios
}

void loop() {
  // Generar un número aleatorio de 8 dígitos
  long randomNumber = random(10000000, 99999999);

  // Imprimir el número aleatorio
  Serial.println("5555");

  delay(1000);

  
  // Esperar 1 segundo antes de enviar el próximo número
}
