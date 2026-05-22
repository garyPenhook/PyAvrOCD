#include <avr/eeprom.h>
#include "ledsignal.h"

boolean OK = true;

uint8_t ee_data[] EEMEM = "Data that's loaded straight into EEPROM\n";

uint8_t ver[41] = "Data that's loaded straight into EEPROM\n";

int count;

void setup() {
#if FLASHEND > 2048
  Serial.begin(19200);
#endif
  eeprom_write_byte(ee_data, 'd');
  ver[0] = 'd';
}

void loop() {
  char c;
  int i = 0;
  if (count++ < 10) {
    uint8_t *ptr = ee_data;
    while (eeprom_read_byte(ptr)) {
      c = eeprom_read_byte(ptr++);
      if (ver[i++] != c)
        OK = false;
#if FLASHEND > 2048
      Serial.write(c);
#endif
    }
#if FLASHEND > 2048
    Serial.println();
#endif
  } else {
    blink_exit(OK);
  }
}
