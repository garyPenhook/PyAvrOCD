# Supported MCUs

This is the list of all AVR MCUs, which should be compatible with PyAvrOCD. It is extended continuously as the development of PyAvrOCD proceeds. MCUs tested with PyAvrOCD are marked in bold. MCUs known not to work with PyAvrOCD are struck out. Underlined MCUs are sitting on my desk and are waiting to be tested. All other MCUs listed are supposed to be compatible because their close cousins are. However, this assumption can be wrong, as I noticed when developing dw-link.

The list is structured by the Arduino cores that support the chips, where some of the MCUs are supported by more than one core.

## Classic ATtinys

### ATtinys supported by *[MicroCore](supporting-cores.md#microcore)*

- **ATtiny13(A)**

Because of its limited flash memory, debugging a sketch on this MCU is rather challenging.

### ATtinys supported by *[TinyCore](supporting-cores.md#tinycore)* and *[ATTinyCore (Debug enabled)](supporting-cores.md#attinycore-debug-enabled)*

* **ATtiny43U**
* **ATtiny2313, ATtiny2313A, ATtiny4313**
* **ATtiny24(A), ATtiny44(A), ATtiny84(A)**
* **ATtiny441**, **ATtiny841**
* **ATtiny25, ATtiny45, ATtiny85**
* **ATtiny261(A), ATtiny461(A), ATtiny861(A)**
* **ATtiny87**, **ATtiny167**
* **ATtiny828**
* **ATtiny48, ATtiny88**
* **ATtiny1634**

### Other ATtinys without a debug interface

- <s>ATtiny4, ATtiny5, ATtiny9, ATtiny10</s>
- <s>ATtiny11, ATtiny12, ATtiny15</s>
- <s>ATtiny20 </s>, <s>ATtiny40</s>
- <s>ATtiny22</s>
- <s>ATtiny26</s>
- <s>ATtiny28</s>
- <s>ATtiny102, ATtiny104</s>

## Modern ATtinys

There is no support for the tinyAVR 0-, 1-, and 2-series devices yet. But this will change shortly.

## Classic ATmegas

### ATmegas supported by [*MiniCore*](supporting-cores.md#minicore)

- <s>ATmega8</s>

* **<s>ATmega48</s>,** **ATmega48A,** **ATmega48P**, **ATmega48PA,** **ATmega48PB**,
* **<s>ATmega88</s>,** **ATmega88A,** **ATmega88P**, **ATmega88PA,** **Atmega88PB**,
* **ATmega168,** **ATmega168A**, **ATmega168P**, **ATmega168PA**, **ATmega168PB**,
* **ATmega328,** **ATmega328P**, **ATmega328PB**

The ATmega8 does not possess a debug interface. The ATmega48 and ATmega88 (without the A-suffix) sitting on my desk suffer from the problem that they either cannot be switched to debugWIRE mode, or, if you are successful, they become unresponsive. I suspect that this applies to all chips labeled this way. Even chips recently purchased through an official distributor had these issues. For this reason, PyAvrOCD will identify these chips and refuse to handle them.

### ATmegas supported by [*XMiniCore*](supporting-cores.md#xminicore)

The following MCUs are already supported by MiniCore. However, XMiniCore goes some way to make it easier to deal with the Microchip Xplained Mini development boards so that debugging becomes plug-and-play.

- **ATmega328P** (Xplained Mini board)
- **ATmega168PB** (Xplained Mini board)
- **ATmega328PB** (Xplained Mini board)

### ATmegas supported by [*MightyCore*](supporting-cores.md#mightycore)

* **ATmega16(A)**, **ATmega32(A)**
* **ATmega164(P)(A)**, **ATmega324(P)(A)**, **ATmega324PB**, **ATmega644(P)(A)**, **ATmega1284(P)**
* <s>ATmega8535</s>

The ATmega16 MCUs (with and without an A-suffix) have a stuck-at-one-bit in the program counter, which may lead to problems when you use an unpatched version of AVR-GDB. In this case, backtraces are garbled, and line-stepping might not work as expected. Use the AVR-GDB version shipped with PyAvrOCD instead, which can also be downloaded from the [Releases page of my avr-gdb repo](https://github.com/felias-fogg/avr-gdb/releases/latest).

The ATmega8535 does not possess a debug interface.

### ATmegas supported by [*MegaCore*](supporting-cores.md#megacore)

* **ATmega64(A)**, **ATmega128(A)**
* **ATmega640**, **ATmega1280**, **ATmega2560**
* **ATmega1281**, **ATmega2561**
* **ATmega165(P)(A)**, **ATmega325(P)(A)**, **ATmega645(P)(A)**
* **ATmega169(P)(A)**, **ATmega329(P)(A)**, **ATmega649(P)(A)**
* **ATmega3250(P)(A)**, **ATmega6450(P)(A)**
* **ATmega3290(P)(A)**, **ATmega6490A**
* **AT90CAN32**, **AT90CAN64**, **AT90CAN128**

The Atmega64(A), ATmega329(P)(A), and ATmega3250(P)(A) MCUs have a stuck-at-one-bit in the PC, which might lead to the same problem as for the ATmega16s mentioned above when an older, unpatched AVR-GDB version is used.

The ATmega128(A) MCUs do not allow for software breakpoints. This means that you can use only four hardware breakpoints.

### ATmega supported by [*MajorCore*](supporting-cores.md#majorcore)

* **ATmega162**
* <s>ATmega8515</s>

The ATmega8515 does not have a debug interface.

### Other ATmegas with debugWIRE interface

* <u>ATmega8U2</u>, ATmega16U2, <u>ATmega32U2</u>
* ATmega32C1, ATmega64C1, ATmega16M1, <u>ATmega32M1</u>, <u>ATmega64M1</u>
* AT90USB82, **AT90USB162**
* AT90PWM1, <u>AT90PWM2B</u>, AT90PWM3B
* <u>AT90PWM81</u>, AT90PWM161
* <u>AT90PWM216</u>, AT90PWM316
* <u>ATmega8HVA</u>, ATmega16HVA, <u>ATmega16HVB</u>, ATmega32HVB, ATmega32HVBrevB, ATmega64HVE2

### Other ATmegas with JTAG interface

* ATmega16U4, **ATmega32U4**
* AT90USB646, AT90USB647, <u>AT90USB1286</u>, AT90USB1287
* ATmega644rfr2, ATmega1284rfr2, ATmega2564rfr2
* ATmega64rfr2, ATmega128rfr2, <u>ATmega256rfr2</u>
* ATmega128rfa1
* ATmega406

## Modern ATmegas

### Atmegas supported by *[MegaCoreX](supporting-cores.md#megacorex)*

This is the megaAVR 0-series. The ATmega4809 made it on some Arduino boards.

- <u>ATmega808</u>, ATmega1608, <u>ATmega3208</u>, **ATmega4808**
- <u>ATmega809</u>, ATmega1609, ATmega3209, **ATmega4809**

## AVR-Dx devices

No support yet.

## XMegas

There is no support yet for XMegas. Since they are not supported by any active Arduino core and do not have any support in PlatformIO, the chances are not very high that I will dive into that.
