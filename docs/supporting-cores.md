# Installing a debug-enabled Arduino core

Arduino cores or platforms are the means to support MCUs and boards for integration into the Arduino IDE 2 (and into the Arduino CLI). They are the key to making debugging for particular chips available in the Arduino IDE 2. Meanwhile, there exists a number of debug-enabled Arduino cores. Sometimes, they are forks, sometimes improved new versions of older cores, and sometimes they are extensions of existing cores. Note that PyAvrOCD can support an MCU, but there is no corresponding core. This means that debugging by means of GDB is possible, but there is no Arduino IDE support (so far).

If you want to install a core, in most cases, you first have to add a *package index*  URL to the list of `Additional boards manager URLs`, which you find in the `Preferences` dialog. Once this has been done, you can search in the `Boards Manager` (accessible through the `Tools` menu or the board icon on the left side of the Arduino IDE 2 window) for the core, and then install it.

### [ATTinyCore (Debug enabled)](https://github.com/felias-fogg/ATTinyCore)

This is my fork of Spence Konde's ATTinyCore version 1.5.2, which covers all classic ATtinys with a debugWire interface. With the advent of TinyCore (see below), it is deprecated. You can install it after including the following URL:

```
https://felias-fogg.github.io/ATTinyCore/package_drazzy.com_ATTinyCore_index.json
```

### [TinyCore](https://github.com/MCUdude/TinyCore)

This is a fork of Spence Konde's ATTinyCore version 2.0.0. It is the preferred way of supporting classic ATtinys.  It does not support the micronucleus bootloader, however. You can install it after including the following URL:

```
https://mcudude.github.io/TinyCore/package_MCUdude_TinyCore_index.json
```

### [MicroCore](https://github.com/MCUdude/MicroCore)

This is a core for the ATtiny13(A). You can make it installable by adding the following URL to the Boards Manager URLs:

```
https://mcudude.github.io/MicroCore/package_MCUdude_MicroCore_index.json
```

### [MiniCore](https://github.com/MCUdude/MiniCore)

This is the core for the small ATmegas with a debugWIRE interface, aka, ATmegaX8.  You can make it installable by adding the following boards manager URL:

```
https://mcudude.github.io/MiniCore/package_MCUdude_MiniCore_index.json
```

### [XMiniCore](https://github.com/felias-fogg/XMiniCore)

This is a debug-enabled Arduino core for the Microchip development boards [ATmega328P Xplained Mini](https://www.microchip.com/en-us/development-tool/atmega328p-xmini), [ATmega168BP Xplained Mini](https://www.microchip.com/en-us/development-tool/atmega168pb-xmini), and [ATmega328PB Xplained Mini](https://www.microchip.com/en-us/development-tool/atmega328pb-xmini). It is meant to be a replacement for the *Atmel AVR Xplained-minis* board package of the official Arduino distribution, which is already 10 years old and does not really work. The new core is a stripped-down and adapted version of MCUdude's MiniCore. The boards, together with PyAvrOCD, work very smoothly. It is just plug-and-play:

```
https://felias-fogg.github.io/XMiniCore/package_felias-fogg_XMiniCore_index.json
```

### [MightyCore](https://github.com/MCUdude/MightyCore)

An Arduino core for ATmega8535, ATmega16, ATmega32, ATmega164, ATmega324, ATmega644, and ATmega1284, whereby ATmega8353 does not have a debugging interface. You can make it installable by adding the following boards manager URL:

```
https://mcudude.github.io/MightyCore/package_MCUdude_MightyCore_index.json
```

### [MegaCore](https://github.com/MCUdude/MegaCore)

A core for most 64 and 100-pin AVRs. All of the listed MCUs are debuggable, but the ATmega128 has the problem that only hardware breakpoints are allowed. You can make the core installable by adding:

```
https://mcudude.github.io/MegaCore/package_MCUdude_MegaCore_index.json
```

### [MajorCore](https://github.com/MCUdude/MajorCore)

This core covers just ATmega8515 and ATmega162, of which only the latter possesses a debugging interface. The additional board manager URL is:

```
https://mcudude.github.io/MajorCore/package_MCUdude_MajorCore_index.json
```

### [MegaCoreX](https://github.com/MCUdude/MegaCoreX)

This is an **experimental** fork of the core for the megaAVR-0 chip family, such as the ATmega4809, which is used on the Nano Every Board and the Uno WiFi Rev 2. You can install the core (note: **this is a work in progress!**) using the following URL:

```
https://felias-fogg.github.io/MegaCoreX/package_MCUdude_MegaCoreX_index.json
```

The debug support for this core might not be bug-free (no pun intended). If you spot a bug, please report it.
