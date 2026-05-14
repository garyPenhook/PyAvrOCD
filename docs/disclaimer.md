# Disclaimer

Note that, as is usual in life, there are some risks involved when using a tool. In particular, [the debugWIRE interface can be a serious health risk to your MCU](limitations.md#debugwire-can-brick-mcus). Even worse, all other aspects of the debugging package have the potential of doing harm to the tested MCU or its environment. [Flash wear](limitations.md#flash-wear), for instance, is an issue when you use software breakpoints.  Moreover, the user of a debugger may also be in danger because debugging can drive you crazy. Sometimes [the debugger itself appears to be buggy](limitations.md#compiler-bugs), sometimes [bugs might disappear](limitations.md#disappearing-bugs), or [bugs appear out of thin air](limitations.md#bugs-appearing-out-of-thin-air) while debugging.

Further, the debug probe, the PyAvrOCD server, and the GDB debugger have a [number of limitations](limitations.md), which may lead to a behavior of the MCU that differs from when no debugger is present. Finally, using a debugger on an MCU that controls a system in real-time can lead to funny results. So, be careful when debugging your microcontroller-controlled brewery.

!!! info "No warranty!"
    All in all, bear in mind that [the software is provided "as is", without warranty of any kind](license-link.md).

