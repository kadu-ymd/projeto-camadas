#define TX_PIN 6  // Pino de transmissão
#define BAUD_RATE 9600
bool enviado = false;
int nClocks = 1667;

void setup() {
  pinMode(TX_PIN, OUTPUT);
  digitalWrite(TX_PIN, HIGH);  // Define o nível inicial como alto
  Serial.begin(BAUD_RATE);     // Inicializa a comunicação serial
}

byte dados = 0xA1;

void atraso(int tempo = nClocks){
  for (int i=0; i<tempo; i++) asm("NOP");
}

void loop() {
  if (!enviado) {
    // Inicia a transmissão: Start Bit (0)
    digitalWrite(TX_PIN, LOW);  // Inicia a transmissão (nível baixo)
    atraso();    // Aguarde um curto período de tempo

    // Envia os dados
    int cont = 0;
    for (int j = 0; j < 8; j++) {
      byte pronto = (dados >> j) & 0x01;
      if (pronto == 1) {
        cont++;
      };
      digitalWrite(TX_PIN, pronto);
      atraso();
    };
    digitalWrite(TX_PIN, 0);
    atraso();

    // Finaliza a transmissão: Stop Bit (1)
    digitalWrite(TX_PIN, HIGH);  // Volta o nível para alto

    delay(2);                 // Aguarda 1 segundo antes de enviar novamente
    enviado = true;

    Serial.println(dados);
  }
}
