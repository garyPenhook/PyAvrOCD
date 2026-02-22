# Notes about extending PyAvrOCD to UPDI



## General registers and I/O registers

For UPDI targets, addressing of general registers and I/O registers is a bit different from that of JTAG/dw targets:

1. General registers are not addressable as SRAM locations
2. I/O registers are addressed in the usual way in In/Out instructions. However, for ordinary LD/ST direct and indirect addressing, the -0x20 offset for I/O instructions does not apply!

This means

- that in `_filter_unsafe_instruction` in `breakexec.py`, `SREGADDR` needs to be different and the -0x20 does not apply.

- set SREGADDR according to device type

- set IO_offset according to device type

- Check for all places where we use SRAM reads/writes to read/write registers

- We need to have special read/write register functions in xavrdebug, which will "buffer" reads and writes and in the background use register file_read and _write (just before execution/singlestepping starts)





The lower end of the user SRAM (and therefore stack) for UPDI targets is much higher than that of JTAG/dw, i.e.,

- `_stack_pointer_legal` should test against a much higher address. Perhaps, we can just ignore it.



The role of shadow regs in the OCD area is not entirely clear! Do we have to write to them in order to change the regs? I believe not. But this needs to be tested.