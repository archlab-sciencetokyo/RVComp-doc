# bootrom

## Overview

bootrom is a ROM that stores the first-stage bootloader and device tree executed first after startup. It uses BRAM. Here, mainly the software part is explained. The hardware part implements just a ROM and an interconnect slave.

## Module Hierarchy

Hardware
```
bootrom (bootrom/bootrom.v)                # ROM for boot (no submodules)
```


Software
```
src/
├── bootrom.S                              # Startup routine
├── bootloader.c                           # First-stage bootloader
├── rvcom_uart.c                           # UART driver implementation
├── rvcom_uart.h                           # UART driver header
├── io.h                                   # I/O macros
└── linker.ld                              # Linker script
```

Device Tree
```
rvcom.dts (rvcom.dtb)                      # Device tree
```

### Key Features

- **Size**: 8KiB
- **Memory Type**: ROM
- **Address Range**: 0x00010000 - 0x00012000
- **First-stage Bootloader**: Load kernel from UART to DRAM

### Module Description

#### bootrom (bootrom/bootrom.v)
bootrom is read-only memory using BRAM. It has 8KB capacity and stores the first-stage bootloader and device tree. After reset, the CPU's program counter (PC) is set to 0x00010000, and instruction fetching begins from here.
bootrom stores in 128-bit units and is read with 128-bit data width. An interconnect slave is implemented.


## Software Configuration

Bootrom software is stored in the `rvcom/bootrom/src/` directory:

### bootrom.S
Executes startup routine and calls the first-stage bootloader.
Then starts OpenSBI, the second-stage bootloader, passing the device tree and hartid to identify the CPU as arguments.
### bootloader.c

First-stage bootloader program that loads program image from UART to DRAM.
Displays "[     bootrom] Hello, world!\n" and receives `BIN_SIZE` bytes of data specified in Makefile from UART and writes to DRAM.


### rvcom_uart.c / rvcom_uart.h

UART control driver.
Use these functions to perform UART read/write operations.

### io.h

Inline assembly macros for hardware I/O.
CPU accesses via MMIO, so uses lw/sw.

### linker.ld

Linker script for bootrom.
Describes address placement for MMIO access, etc.
