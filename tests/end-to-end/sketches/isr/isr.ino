#include <Arduino.h>
#include <util/delay.h>
#include "irqpin.h"

volatile int irqcount = 0;
volatile int outsidecount = 0;


void setup()
{
#if FLASHEND >= 4095
  Serial.begin(38400);
  Serial.println(F("Startup ..."));
  _delay_ms(500);
#endif
  pinMode(IRQPIN, OUTPUT);
  digitalWrite(IRQPIN, LOW);
  attachInterrupt(digitalPinToInterrupt(IRQPIN), irqserver, LOW);
}

void loop()
{
  int pcount;
  digitalWrite(IRQPIN, LOW);
  shortwait();
  outsidecount++;
  digitalWrite(IRQPIN, HIGH);
  _delay_ms(200); // necessary to give enough time for printing!
#if FLASHEND >= 4095
  Serial.print("IRQ count: ");
  pcount = irqcount;
  Serial.println(pcount);
#endif
}

void shortwait()
{
  _delay_ms(0.0001);
}

void irqserver()
{
  irqcount++;
}
