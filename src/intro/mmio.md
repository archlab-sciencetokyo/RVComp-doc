# Memory Mapped Region

This section explains the memory map and Memory-Mapped I/O (MMIO) of the RVComp system. RVComp has a 34-bit physical address space, with memory and peripherals mapped to specific address ranges.

## Memory Map Overview

RVComp's physical memory map is configured as follows:

| **Address Range**            | **Device/Region**      |
|:----------------------------:|:----------------------:|
| 0x0001_0000 - 0x0001_1FFF    | Boot ROM               |
| 0x0200_0000 - 0x020B_FFFF    | CLINT                  |
| 0x0C00_0000 - 0x0CFF_FFFF    | PLIC                   |
| 0x1000_0000 - 0x1000_00FF    | UART                   |
| 0x8000_0000 - 0x87FF_FFFF    | DRAM (Nexys4DDR)       |
| 0x8000_0000 - 0x8FFF_FFFF    | DRAM (ArtyA7)          |

For details on each item, please refer to [SoC Architecture](../arch/index.md).
