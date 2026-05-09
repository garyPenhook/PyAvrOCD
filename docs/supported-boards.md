# Supported boards

Almost all boards equipped with one of the supported chips can be used in one way or another. Tested boards are marked in boldface, and those known not to work are struck out. The ones that are underlined are sitting on my desk and are waiting to be tested. If no core is mentioned, then there is no support through an Arduino core yet, but PyAvrOCD nevertheless supports debugging the chip.

For supported boards, possible board modifications and other information is mentioned.


## Microchip boards

Most of the supported Microchip boards have an embedded debugger on board, which makes it easy to work with. You do not have to modify the boards physically or change fuses. When working with debugWIRE targets, the power cycling is done automatically.

- **ATmega328P** **Xplained Mini**:  [XMiniCore](supporting-cores.md#xminicore); onboard debugger, no physical modifications or fuse settings necessary,  power-cycling is automatic.
- **ATmega168PB** **Xplained Mini**: [XMiniCore](supporting-cores.md#xminicore); onboard debugger, no physical modifications or fuse settings necessary,  power-cycling is automatic.
- **ATmega328PB** **Xplained Mini**: [XMiniCore](supporting-cores.md#xminicore); onboard debugger, no physical modifications or fuse settings necessary,  power-cycling is automatic.
- **ATmega324PB Xplained Pro:** [MightyCore](supporting-cores.md#mightycore); onboard debugger, serial I/O is routed via `Serial1` instead of `Serial`; the LED is connected to digital pin 23. No physical modifications or fuse settings necessary.
- <u>AT90USBKEY2 (AT90USB1287)</u>
- <u>ATmega256RFR2 Xplained Pro</u>
- **AVR Butterfly (ATmega169)**: [MegaCore](supporting-cores.md#megacore)
- <u>MEGA-1284P Xplained</u>: [MightyCore](supporting-cores.md#mightycore)
- **ATmega4809 Curiosity Nano**: [MegaCoreX](supporting-cores.md#megacorex); onboard debugger; choose the `48 pin standard` pinout; serial I/O is routed via `Serial3`; the LED is connected to PF5 (digital pin 39); the programmer you have to choose is `Curiosity Nano`.
- ATtiny416 Xplained Nano:  [megaTinyCore (fork)](https://github.com/felias-fogg/megaTinyCore); onboard debugger
- ATtiny817 Xplained Pro: [megaTinyCore (fork)](https://github.com/felias-fogg/megaTinyCore); onboard debugger
- <u>ATtiny817 Xplained Mini</u>: [megaTinyCore (fork)](https://github.com/felias-fogg/megaTinyCore); onboard debugger
- **ATtiny1607 Curiosity Nano**: [megaTinyCore (fork)](https://github.com/felias-fogg/megaTinyCore); onboard debugger; LED is connected to PB7; Button is on PC4; programmer should be `Curiosity Nano`; serial I/O through the debug interface does not seem to work.
- ATtiny1627 Curiosity Nano:  [megaTinyCore (fork)](https://github.com/felias-fogg/megaTinyCore); onboard debugger
- ATtiny3217 Curiosity Nano: [megaTinyCore (fork)](https://github.com/felias-fogg/megaTinyCore); onboard debugger
- **ATtiny3227 Curiosity Nano**: [megaTinyCore (fork)](https://github.com/felias-fogg/megaTinyCore); onboard debugger; LED is connected to PB7; Button is on PC4; programmer should be `Curiosity Nano`; serial I/O through the debug interface does not seem to work.

## Arduino boards


- Arduino Yún
- **Arduino UNO R3**:   [MiniCore](supporting-cores.md#minicore); [the `RESET EN` solder bridge needs to be cut](board-preparation.md#preparing-a-debugwire-target)
- Arduino UNO Mini:  [MiniCore](supporting-cores.md#minicore); remove capacitor `C3`
- Arduino Duemilanove:  [MiniCore](supporting-cores.md#minicore); `RESET EN` needs to be cut
- Arduino Diecimila:  [MiniCore](supporting-cores.md#minicore); [remove 100nF capacitor](https://awtfy.com/2010/02/21/modify-an-arduino-for-debugwire/)
- **Arduino Nano:**  [MiniCore](supporting-cores.md#minicore); [100 nF cap and 1kΩ resistor needs to be removed](board-preparation.md#arduino-nano-and-clones)
- **Arduino Mega**: [MegaCore](supporting-cores.md#megacore); JTAG pins are A4-A7, use [this board adapter](https://github.com/felias-fogg/PyAvrOCD/tree/main/pcbs/arduino-jtag), `RESET EN` does not need to be opened
- **Arduino Mega 2560:** [MegaCore](https://github.com/MCUdude/MegaCore); JTAG pins are A4-A7, use [this board adapter](https://github.com/felias-fogg/PyAvrOCD/tree/main/pcbs/arduino-jtag), `RESET EN` does not need to be opened
- Arduino Mega ADK: [MegaCore](supporting-cores.md#megacore)
- **Arduino Leonardo**: JTAG pins are A0-A3, use [this board adapter](https://github.com/felias-fogg/PyAvrOCD/tree/main/pcbs/arduino-jtag)
- Arduino Leonardo ETH
- <u>Arduino Micro</u>
- <s>Arduino Esplora</s>: JTAG pins are not accessible
- Arduino Mini: [MiniCore](supporting-cores.md#minicore) (if Mini 05); do not connect the DTR pin of the FTDI header
- Arduino Ethernet: [MiniCore](supporting-cores.md#minicore); do not connect the DTR pin of the FTDI header
- <u>Arduino Fio</u>:  [MiniCore](supporting-cores.md#minicore); do not connect the DTR pin of the FTDI header, and do not connect an XBee
- Arduino BT:  [MiniCore](supporting-cores.md#minicore); remove capacitor `C1` (which you do not have to resolder after debugging)
- <s>LilyPad Arduino USB</s>: JTAG pins are not accessible
- <u>LilyPad Arduino</u>:  [MiniCore](supporting-cores.md#minicore); do not connect the DTR pin of the FTDI header
- <u>Arduino Pro</u>:  [MiniCore](supporting-cores.md#minicore); do not connect the DTR pin of the FTDI header
- <u>Arduino Pro Mini</u>:  [MiniCore](supporting-cores.md#minicore); do not connect the DTR pin of the FTDI header
- Arduino NG (ATmega168):  [MiniCore](supporting-cores.md#minicore); no modifications necessary
- <s>Arduino NG (ATmega8)</s>: no debugging interface
- Arduino Robot Control
- Arduino Robot Motor
- <u>Arduino Gemma</u>: [TinyCore](supporting-cores.md#tinycore); RESET pad on backside
- <u>Adafruit Circuit Playground 32u4</u>
- Arduino Yún Mini
- Arduino Industrial 101
- Arduino Linino One
- Arduino UNO WiFi (Rev 1):  [MiniCore](supporting-cores.md#minicore); cut `RESET EN` solder bridge
- **Arduino Uno WiFi (Rev 2)**: [MegaCoreX](supporting-cores.md#megacorex); board has an onboard debugger; the recommended pinout is `Uno Wifi`; serial I/O is via `Serial`; `LED_BUILTIN` is digital pin 25 (PD6); there is no bootloader support because you can load via the onboard debugger/programmer `microUPDI/Uno WiFi`
- **Arduino Nano Every:** [MegaCoreX](supporting-cores.md#megacorex); [UPDI pad on the backside](board-preparation.md#preparing-a-updi-target); the only pinout is `Nano Every`; serial I/O is routed via `Serial`; `LED_BUILTIN` is digital pin 13 (PE2); there is no bootloader support because you can load via the onboard programmer `JTAG2UPDI`

## Sparkfun boards

- RedBoard (ATmega328P): [MiniCore](supporting-cores.md#minicore), remove `C8`
- <u>Pro Micro 3.3V (ATmega32U4)</u>
- <u>Pro Micro 5V (ATmega32U4)</u>
- Fio v3
- Qduino Mini (ATmega32U4)
- Mega Pro 3.3V: [MegaCore](supporting-cores.md#megacore)
- Mega Pro 5V: [MegaCore](supporting-cores.md#megacore)
- RedBot (ATmega328P): [MiniCore](supporting-cores.md#minicore)
- <u>Serial-7-Segment-Display</u> (ATmega328P): [MiniCore](supporting-cores.md#minicore)
- ATmega128RFA1 Development Board
- <s>LilyPad USB Plus</s>:  JTAG pins are not accessible
- SerLcd
- Digital Sandbox (ATmega328P): [MiniCore](supporting-cores.md#minicore)
- Microview (ATmega328P): [MiniCore](supporting-cores.md#minicore); the SPI pins are not exposed, you need to solder to some vias inside the enclosure

## Adafruit boards

- <s>Flora (ATmega32U4)</s>: JTAG pins are not accessible
- Feather 32U4
- Feather 328P: [MiniCore](supporting-cores.md#minicore)
- Gemma (ATtiny85):  [TinyCore](https://github.com/MCUdude/TinyCore),
- Trinket 3.3V (ATtiny85): [TinyCore](supporting-cores.md#tinycore)
- Trinket 5V (ATtiny85): [TinyCore](supporting-cores.md#tinycore)
- Metro (ATmega328P):  [MiniCore](supporting-cores.md#minicore), cut `RESET EN` solder bridge
- Metro Mini V2:  [MiniCore](supporting-cores.md#minicore), you have to figure out which cap to remove
- Circuit Playground Classic (ATmega32U4)
- Pro Trinket 5V/16MHz (USB): [MiniCore](supporting-cores.md#minicore)
- Pro Trinket 3V/12MHz (USB): [MiniCore](supporting-cores.md#minicore)
- Pro Trinket 5V/16MHz (FTDI): [MiniCore](supporting-cores.md#minicore)
- Pro Trinket 3V/12MHz (FTDI): [MiniCore](supporting-cores.md#minicore)
- ItsyBitsy 32u4 (3V)
- <u>ItsyBitsy 32u4 (5V)</u>
- Bluefruit Micro
- ATmega32u4 Breakout Board
- **SEESAW Breakout ATtiny817**
- **SEESAW Breakout ATtiny1616**

## Teensy boards

- <u>Teensy 2.0 (ATmega32U4)</u>
- <u>Teensy++ (AT90USB1286)</u>

## Olimex boards

- Olimex-328: [MiniCore](supporting-cores.md#minicore)
- Olimex-32u4
- <s>eduArdu</s>: JTAG pins are not accessible
- Olimex-Nano: [MiniCore](supporting-cores.md#minicore)
- RGB-Glasses
- Olimexino-2560: [MegaCore](supporting-cores.md#megacore)
- **AVR-CAN (AT90CAN128)**: [MegaCore](supporting-cores.md#megacore)
- AVR-GSM (ATMega32): [MightyCore](supporting-cores.md#mightycore)
- AVR-IO-M16 (ATmega16): [MightyCore](supporting-cores.md#mightycore)
- **AVR-MT128 (ATmega128)**: [MegaCore](supporting-cores.md#megacore)
- AVR-USB-STK (AT90USB162)
- **AVR-USB-162 (AT90USB162)**

## Seeed Studio boards

- Seeeduino V3.0: [MiniCore](supporting-cores.md#minicore)
- <u>Seeeduino v4</u>:  [MiniCore](supporting-cores.md#minicore); remove `C14` and RESET LED (next to RESET button)
- <u>Stalker</u>: [MiniCore](supporting-cores.md#minicore); do not connect DTR
- Seeeduino Lotus: [MiniCore](supporting-cores.md#minicore); remove `C6` and RESET LED (next to RESET button)
- Seeeduino Lite
- Seeeduino Nano: [MiniCore](supporting-cores.md#minicore)
- Seeeduino Mega 2560: [MegaCore](supporting-cores.md#megacore)

## Azduino boards by Spence Konde

- **ATtiny841 dev. board**: [TinyCore](supporting-cores.md#tinycore)

- **ATtiny1634 dev. board**: [TinyCore](supporting-cores.md#tinycore)

- **ATtiny88 breakout board (assembled)**: [TinyCore](supporting-cores.md#tinycore)

- **ATtiny828 breakout board (assembled)**: [TinyCore](supporting-cores.md#tinycore)

- **ATtiny167 dev. board**: [TinyCore](supporting-cores.md#tinycore)

- **ATtiny43 dev. board**: [TinyCore](supporting-cores.md#tinycore)

<!--

- <u>ATtiny3217 breakout board (assembled)</u>

-->

## Miscellaneous boards

- <u>MH-ET LIVE (ATtiny88)</u>: [TinyCore](supporting-cores.md#tinycore)
- <u>Digispark (ATtiny85)</u>: [TinyCore](supporting-cores.md#tinycore)
- <u>Digispark Pro (ATtiny167)</u>: [TinyCore](supporting-cores.md#tinycore)
- <u>Pololu A-Star 328PB Micro</u>: [MiniCore](supporting-cores.md#minicore)
- **Thinary Nano Every (ATmega4808)**: [MegaCoreX](supporting-cores.md#megacorex); the only supported pinout is `Nano 4808`; serial I/O via `Serial`; `LED_BUILTIN` is digital pin 9 (PA7); no bootloader support because there is a `JTAG2UPDI` programmer on board
