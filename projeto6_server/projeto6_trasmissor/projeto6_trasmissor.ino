#define RX_PIN 13  // Pino de recepção
#define BAUD_RATE 9600
uint8_t dados;
uint8_t bitParidade;
uint8_t rxParidade;

void setup() {
  pinMode(RX_PIN, INPUT);
  Serial.begin(BAUD_RATE);  // Inicializa a comunicação serial
}

void loop() {
  int cont = 0;

  while (digitalRead(RX_PIN) == HIGH)
    ;

  delayMicroseconds(156);

  for (int i = 0; i < 8; i++) {
    dados |= (digitalRead(RX_PIN) << i);
    if ((digitalRead(RX_PIN) << i) == 1) cont++;
    delayMicroseconds(104);
  }

  rxParidade = digitalRead(RX_PIN);

  if (rxParidade == cont % 2) {
    Serial.println(dados, HEX);
    Serial.println("Bit Paridade OK");
  } else {
    Serial.println(dados, HEX);
    Serial.println("Bit Paridade errado");
  }
}