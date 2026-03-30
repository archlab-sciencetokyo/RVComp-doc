# bootrom

## Overview

bootrom is a ROM that stores the first-stage bootloader and device tree executed first after startup. It uses BRAM. This page focuses mainly on the software side; the hardware side is a ROM plus an interconnect slave.

The bootloader supports two build-time modes:

- **UART boot**
- **MMC (microSD card) boot**

The mode is selected when the bootrom is built. In practice, `tools/setting.py` comments or uncomments `#define UART_BOOT` in `bootrom/src/bootloader.c` so that the generated bitstream matches the selected boot method.

## Module Hierarchy

Hardware

```text
bootrom (bootrom/bootrom.v)                # ROM for boot (no submodules)
```

Software

```text
src/
├── bootrom.S                              # Startup routine
├── bootloader.c                           # First-stage bootloader
├── rvcomp_uart.c                          # UART driver implementation
├── rvcomp_uart.h                          # UART driver header
├── rvcomp_mmc.c                           # sdcram CSR access helpers
├── rvcomp_mmc.h                           # sdcram CSR definitions
├── rvcomp_ether.c                         # Bare-metal Ethernet helper
├── rvcomp_ether.h                         # Bare-metal Ethernet definitions
├── io.h                                   # I/O macros
└── linker.ld                              # Linker script
```

Device Tree

```text
rvcomp.dts (rvcomp.dtb)                    # Device tree
```

### Key Features

- **Size**: 8 KiB
- **Memory Type**: ROM
- **Address Range**: 0x00010000 - 0x00011fff
- **First-stage Bootloader**: Loads `fw_payload.bin` into DRAM either from UART or from the microSD card.

## Module Description

### bootrom (bootrom/bootrom.v)

bootrom is read-only memory using BRAM. It has 8 KiB capacity and stores the first-stage bootloader and device tree. After reset, the CPU's program counter (PC) is set to `0x00010000`, and instruction fetching begins from here.

The ROM stores data in 128-bit units and is read with 128-bit width through the interconnect.

## Software Configuration

Bootrom software is stored in `RVComp/bootrom/src/`.

### bootrom.S

Executes the startup routine and calls the first-stage bootloader. After the payload has been copied into DRAM, control continues to OpenSBI.

### bootloader.c

`bootloader.c` copies `BIN_SIZE` bytes to DRAM at `0x80000000`.

**UART boot mode**:

- Prints `[     bootrom] Hello, world!\n`
- Receives `BIN_SIZE` bytes over UART
- Writes the received bytes to DRAM

This is the mode used by `uv run term --linux-boot`, which starts sending `fw_payload.bin` after it detects the bootrom banner.

**MMC boot mode**:

- Copies `BIN_SIZE` bytes from the beginning of the microSD card into DRAM

Before booting, write the payload and root filesystem to the microSD card and insert it into the Nexys 4 DDR.

### rvcomp_uart.c / rvcomp_uart.h

Baremetal UART driver.

### rvcomp_mmc.c / rvcomp_mmc.h

Baremetal sdcram driver.

### rvcomp_ether.c / rvcomp_ether.h

Baremetal ethernet control drivers.

### io.h

Inline assembly macros for hardware I/O. CPU access is via MMIO, so the macros use load/store instructions.

### linker.ld

Linker script for the bootrom. It describes code placement and MMIO-related address layout.


