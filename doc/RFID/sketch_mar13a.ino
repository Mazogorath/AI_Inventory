#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 5  // RC522의 RST 핀
#define SS_PIN 9  // RC522의 SDA(SS) 핀

MFRC522 mfrc522(SS_PIN, RST_PIN);  // MFRC522 객체 생성

void setup() {
  Serial.begin(9600);  // 시리얼 통신 시작
  SPI.begin();          // SPI 통신 시작
  mfrc522.PCD_Init();   // RC522 초기화
  // Serial.println("Scan RFID tag to get UID");
}

void loop() {
  // RFID 태그 감지 여부 확인
  if ( ! mfrc522.PICC_IsNewCardPresent() || ! mfrc522.PICC_ReadCardSerial()) {
    delay(50);
    return;
  }

  // UID 값 읽어오기
  MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
  // Serial.print("Tag Type: ");
  // Serial.println(mfrc522.PICC_GetTypeName(piccType));

  // UID 값 출력
  // Serial.print("UID Size: ");
  // Serial.println(mfrc522.uid.size);
  // Serial.print("UID Value: ");
  String tagUID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    // Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    // Serial.print(mfrc522.uid.uidByte[i], HEX);
    tagUID.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""));
    tagUID.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println(tagUID);

  delay(100);  // 0.1초 대기 후 다시 감지
}
