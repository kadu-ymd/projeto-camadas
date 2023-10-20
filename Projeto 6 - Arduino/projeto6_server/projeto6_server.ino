#define RX_PIN 4  // Pino de recepção
#define BAUD_RATE 9600
byte dados;  // Variável para armazenar o byte recebido
byte bitParidade;
byte rxParidade;

void setup() {
  pinMode(RX_PIN, INPUT);
  Serial.begin(BAUD_RATE);  // Inicializa a comunicação serial
}


void atraso(float tempo = 1) {
  float T = 1 / BAUD_RATE;
  float clockT = 1 / (16 * pow(10, 6));
  int nClocks = floor(T / clockT) + 1;
  for (int i = 0; i < int(nClocks * tempo); i++) {
    asm("NOP");
  }
}

void loop() {
  if (digitalRead(RX_PIN) == LOW) {
    int cont = 0;
    //atraso(1.5);

    for (int i = 0; i < 8; i++) {
      byte bit = digitalRead(RX_PIN);
      atraso();
      dados |= (bit << i);
      Serial.println(dados, BIN);
      
      if (bit == 1) {
        cont++;
      }
    }
    //Serial.println();

    rxParidade = digitalRead(RX_PIN);

    bitParidade = cont % 2;

    // if (bitParidade == rxParidade) {
    //   Serial.println(dados, HEX);
    //   Serial.println("OK");
    // } else {
    //   Serial.println(dados, HEX);
    //   Serial.println("Não OK");
    // }
    //delay(2000);

    
  }
}