#define TX_PIN 4  // Pino de transmissão
#define BAUD_RATE 9600

void setup() {
  pinMode(TX_PIN, OUTPUT);
  digitalWrite(TX_PIN, HIGH);  // Define o nível inicial como alto
  Serial.begin(BAUD_RATE);     // Inicializa a comunicação serial
}

byte confirmaParidade(byte dados) {
  int cont = 0;
  for (int j = 0; j < 8; j++) {
    if ((dados >> j) & 0x01 == 1) {
      cont++;
    }
  }
  if (cont % 2 == 0) {  // Paridade: 0 se par, 1 se ímpar
    return 0x0;
  } else {
    return 0x1;
  }
}

void loop() {
  byte dados = 0xA1;
  //byte paridade = confirmaParidade(dados);
  byte paridade = 0;

  // Inicia a transmissão: Start Bit (0)
  digitalWrite(TX_PIN, LOW);  // Inicia a transmissão (nível baixo)
  delayMicroseconds(1000);    // Aguarde um curto período de tempo


  // Envia os dados
  for (int j = 0; j < 8; j++) {
    digitalWrite(TX_PIN, (dados >> j) & 0x01);
    Serial.print((dados >> j) & 0x01);
    delayMicroseconds(1000);
  };

  Serial.print(" ");
  Serial.print(paridade);

  digitalWrite(TX_PIN, paridade);
  delayMicroseconds(1000);


  Serial.println();

  // Finaliza a transmissão: End Bit (1)
  digitalWrite(TX_PIN, HIGH);  // Volta o nível para alto
  delay(1000);                 // Aguarda 1 segundo antes de enviar novamente
}
