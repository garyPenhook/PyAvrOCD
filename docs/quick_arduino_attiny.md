## Quickstart guide: SNAP & ATtiny85

This quickstart guide demonstrates how to use the Arduino IDE 2 for debugging on an ATtiny85 using the MPLAB SNAP debug probe.


### Required hardware

* SNAP
* USB cable
* ATtiny85 (or any other classic ATtiny or ATmegaX8) as the *target*
* In order to set up the target, you need:
    * a breadboard together with
    * jumper wires (male-to-male)
    * 1 LED
    * 2 resistors (10 kΩ, 1kΩ)
    * 1 capacitor (100 nF)

### Step 1: Install the debug-enabled TinyCore

Add a new *boards manager URL* in the `Preferences` dialog:

	https://mcudude.github.io/TinyCore/package_MCUdude_TinyCore_index.json
{!details-boards-manager-url.md!}

Next you have to install the new core. Activate the `Boards Manager`, select `TinyCore`, and click on `Install`.

{!details-install-core.md!}

!!! info "Linux systems"
    After the installation, users of Linux systems will need to add `udev` rules. Download [https://pyavrocd.io/99-edbg-debuggers.rules](https://pyavrocd.io/99-edbg-debuggers.rules), edit if you want, and copy to `/etc/udev/rules.d/`.

### Step 2: Connect the target with the debug probe

You need to set up the hardware on a breadboard and use a few jumper wires to connect the ATtiny to the debug probe. Note that the notch or dot on the ATtiny is oriented towards the left.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/snap+attiny85.png" width="80%">
</p>



Here is a table of all connections to check that you have made all the connections.

| ATtiny pin#  | SNAP pin | component                           |
| ------------ | -------- | ----------------------------------- |
| 1 (Reset)    | TAUX #6  | 10k resistor to Vcc                 |
| 2 (D3)       | &nbsp;   | &nbsp;                              |
| 3 (D4)       | &nbsp;   | &nbsp;                              |
| 4 (GND)      | GND #3   | red LED (-), decoupling cap 100 nF  |
| 5 (D0, MOSI) | TTDI #7  |                                     |
| 6 (D1, MISO) | PGD #4   |                                     |
| 7 (D2, SCK)  | PGC #5   | 1 k resistor to LED (+)             |
| 8 (Vcc)      | TVDD #2  | 10k resistor, decoupling cap 100 nF |

### Step 3: Load sketch and select board

Load a sketch, e.g., the `Blink` sketch, and select the right board: `Tools -> Board -> TinyCore -> ATtiny85`. If this is a chip is fresh from the factory, you need to adjust for the clock frequency. Choose `1 MHz internal osc.` under `Tools -> Clock`.

### Step 4: Compile the sketch

Activate `Optimize for Debugging` in the `Sketch` menu. This only needs to be done once. Then click on the `Verify` button (checkmark symbol) in the top bar. This will compile the sketch.

### Step 5: Start debugging

Now it is time to start debugging by clicking the `Debug` button (bug in front of a triangle) in the top bar. If the target MCU is not already in debugWIRE mode, the debugger will request 'power cycling'.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/ide-uno-0a.png" width="90%"></p>

Power cycling means to remove the Vcc jumper cable and after a few seconds to reinsert it. After a while, the `DEBUG` pane should open.

### After debugging has finished

When you are done with debugging, you probably want to disable the debugWIRE mode again, because in debugWIRE mode, you cannot use the RESET line or ISP programming. This can be accomplished by using the command `monitor debugwire disable` before you leave the debugger. In addition, you should disable the `Optimize for Debugging` setting because it will, in general, generate more code.

So, after everything has been debugged, what do you do with your newly built debug probe? You don't have to throw it away. You can also use it as an ISP programmer (STK500 v1). In the Arduino IDE, such a programmer is called `Arduino as ISP`.


### What can go wrong?

There is always the chance that something goes south, either debugging does not start at all, or something funny happens while debugging. If so, it is a good idea to have a look at the output in the `gdb-server` console. Messages with the prefix [WARNING] often tell what went wrong. If the status LED is blinking very fast, it means that the debugger has hit an unrecoverable error. Type `monitor info` into the last line of the `Debug Console` in order to find out about the [error number](troubleshooting.md#internal-and-fatal-dw-link-errors). It may also be a good idea to consult the [Troubleshooting](troubleshooting.md) and the [Limitations](limitations.md) sections.

