#define RX_PIN 13  // Pino de recepção
#define BAUD_RATE 9600

void setup() {
  pinMode(RX_PIN, INPUT);
  Serial.begin(BAUD_RATE);  // Inicializa a comunicação serial
}

byte checkParidade(byte b) {
  int cont = 0;
  for (int i = 0; i < 8; i++) {
    if ((b >> i) & 0x01 == 1) {
      cont++;
    }
  }
  if (cont % 2 == 0) {
    return 0x0;
  } else {
    return 0x1;
  }
}

void loop() {
  byte dados;  // Variável para armazenar o byte recebido
  byte bitParidade;
  byte rxParidade;

  // Aguarda o início da transmissão
  while (digitalRead(RX_PIN) == HIGH) {
    // Aguarda até que o nível do pino seja baixo para indicar o início da transmissão
    // Verifica o start bit, se a leitura do pino for 1, inicia a leitura do byte
  }

  delayMicroseconds(1.5/BAUD_RATE);

  for (int i = 0; i < 8; i++) {
    dados |= (digitalRead(RX_PIN) << i);
    delayMicroseconds(1/BAUD_RATE);
  }
  bitParidade = checkParidade(dados);

  Serial.print(dados, HEX);
  Serial.print(" ");

  rxParidade = digitalRead(RX_PIN);
  delayMicroseconds(1/BAUD_RATE);

  if (rxParidade == bitParidade) {
    Serial.print("Bit Paridade OK");
  } else {
    Serial.print("Bit Paridade errado");
  }

  Serial.println();


}