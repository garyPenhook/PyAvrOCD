# Compiling the program

A necessary prerequisite for debugging a program is that you compile it.

## Compiling an Arduino sketch in the Arduino IDE 2

Compiling the Arduino sketch is done by clicking on the Verify button in the top right.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/ide2-1.png" width="70%">
</p>

Before doing that, it is advisable to select the `Optimize for Debugging` option.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/optimize-for-debug.png" width="30%"></p>

This will select the compilation option -`Og` and will disable *link time optimization* in order to make the debugging experience smoother. Otherwise, some variables and structural information may not be displayed, the debugger may not be able to stop at every line, and single-stepping may not necessarily follow the statements as specified in the source text. However, selecting this option can also enlarge the size of the binary code significantly. Experience shows that the growth can be up to 40%. If the resulting binary code does not fit into flash memory, one can also debug with a disabled `Optimize for Debugging` option. However, debugging will in this case be less comfortable.

Once this option has been activated, it will also be enabled for other projects. You have to explicitly disable this option in order to get smaller binary files again.

## Compiling in other environments

In most IDEs and, of course, on the command line, you usually have full control over all the compiler and linker settings. The following ones are critical when debugging:

- The *compiler optimization level* for MCUs is usually `-Os`, meaning that the needed space in flash memory should be minimized. For debugging, one should choose `-Og` instead, which optimizes for space but tries to keep the control flow as similar as in the source text, i.e., no inlining or code re-ordering. Of course, the produced binary will be bigger than when using `-Os`.
- *Link time optimization*, triggered by `-flto` for compilation and linking, will prune away unused library code. In addition, it may also do code inlining across compilation units. Further, it seems to prune debugging information, such as information about global variables and class structures. For this reason, it is advisable to disable link time optimization when debugging.  Again, this will increase the size of the binary.
- *Link time jump relaxation* is triggered by the compiler and linker option `-mrelax`. This will try to replace `JMP` and `CALL` instructions with `RJMP` and `RCALL` at link time. While this sounds like a reasonable and easy optimization, its implementation is unfortunately buggy when it comes to the generation of debugging information. The line number information is completely garbled, at least in version AVR-GCC v7.3. So this option should never be used when debugging.
- *Including debugging information* is triggered by the compiler option `-g`. This may enlarge the size of the object file in ELF format, but does not lead to larger binaries. So, this option can always be used at no cost. Using `-g3` or `-ggdb3`  instead of `-g` promises to record more debugging information, which might be helpful for the debugging process.
