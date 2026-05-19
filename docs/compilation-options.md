# Compiling the program

A necessary prerequisite for debugging a program is that you compile it.

## Compiling an Arduino sketch in the Arduino IDE 2

Compiling the Arduino sketch is done by clicking on the Verify button in the top right.

<p align="center">
<img src="https://raw.githubusercontent.com/felias-fogg/PyAvrOCD/refs/heads/main/docs/pics/ide2-1.png" width="70%">
</p>

Before doing that, it is advisable to select the `Optimize for Debugging` option.

<p align="center"><img src="https://raw.githubusercontent.com/felias-fogg/pyavrocd/refs/heads/main/docs/pics/optimize-for-debug.png" width="30%"></p>

This will select the debugging-friendly optimization option `-Og` in order to make the debugging experience smoother. Otherwise, the debugger may not be able to stop at every line, and single-stepping may not necessarily follow the statements as specified in the source text. However, selecting this option can also enlarge the size of the binary code significantly. Experience shows that the growth is usually around 20%, but can be as bad as 40%. If the resulting binary code does not fit into flash memory, one can also debug with a disabled `Optimize for Debugging` option. However, debugging will in this case be less comfortable.

As an alternative to disabling the `Optimize for Debugging` option when the binary code gets too large, you may consider conditionally disabling parts of your code. When the `Optimize for Debugging` option is active, the compile-time constant `DEBUG` is defined. So you can enclose parts of your code by

```C++
#ifndef DEBUG
...
#endif
```

in order to deactivate this part of your code when the `Optimize for Debugging` option is enabled.

!!! info "Disable 'Optimize for Debugging' setting after debugging has finished."
    Once `Optimize for Debugging` has been activated, it will also be enabled for other projects. You have to explicitly disable this option in order to get smaller binary files again.

For some of the debug-enabled Arduino cores, it is possible to disable *link-time optimization* (`LTO`). This can be helpful because it will preserve some debug information (see below).

## Compiling in other environments

In most IDEs and, of course, on the command line, you usually have full control over all the compiler and linker settings. There are a few compiler options that are critical for debugging.

### Critical optimization options

- The *compiler optimization level* for MCUs is usually `-Os`, meaning that the needed space in flash memory should be minimized. For debugging, one should choose `-Og` instead, which optimizes for space but tries to keep the control flow as similar as possible to the source text, i.e., no inlining or code re-ordering. Of course, the produced binary will be bigger than when using `-Os`.
- *Link time optimization*, enabled by `-flto` for compilation and linking, will prune away dead code. In addition, it may also do code inlining across compilation units. Further, the currently employed GCC  version 7.3.0 prunes debugging information, such as information about global variables and class structures. For this reason, it is advisable to disable link time optimization when debugging.  However, this is not possible for the Arduino cores that support modern AVR MCUs. Hopefully, the situation will improve when upgrading to a more recent GCC version.
- *Link time jump relaxation* is enabled by the compiler and linker option `-mrelax`. This will try to replace `JMP` and `CALL` instructions with `RJMP` and `RCALL` at link time. While it sounds like a reasonable and easy optimization, its implementation is unfortunately buggy when it comes to the generation of debugging information. The line number information is completely garbled, at least in version AVR-GCC v7.3. So this option should *never be used when debugging*.
- *Including debugging information* is enabled by the compiler option `-g`. This may enlarge the size of the object file in ELF format, but does not lead to larger binaries. So, this option can always be used at no cost. Using `-g3` or `-ggdb3`  instead of `-g` will record macro definitions, which might be helpful for the debugging process.

