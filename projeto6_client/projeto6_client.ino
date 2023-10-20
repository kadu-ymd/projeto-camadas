#define TX_PIN 6  // Pino de transmissão
#define BAUD_RATE 9600
bool enviado = false;

void setup() {
  pinMode(TX_PIN, OUTPUT);
  digitalWrite(TX_PIN, HIGH);  // Define o nível inicial como alto
  Serial.begin(BAUD_RATE);     // Inicializa a comunicação serial
}

byte dados = 0xA0;

void loop() {
  if (!enviado) {
    // Inicia a transmissão: Start Bit (0)
    digitalWrite(TX_PIN, LOW);  // Inicia a transmissão (nível baixo)
    delayMicroseconds(104);    // Aguarde um curto período de tempo

    // Envia os dados
    int cont = 0;
    for (int j = 0; j < 8; j++) {
      byte pronto = (dados >> j) & 0x01;
      if (pronto == 1) {
        cont++;
      };
      digitalWrite(TX_PIN, pronto);
      delayMicroseconds(104);
    };
    digitalWrite(TX_PIN, cont%2);
    delayMicroseconds(104);

    // Finaliza a transmissão: Stop Bit (1)
    digitalWrite(TX_PIN, HIGH);  // Volta o nível para alto
    delay(2000);                 // Aguarda 1 segundo antes de enviar novamente
    enviado = true;
    
    Serial.println(dados);
  }
}
