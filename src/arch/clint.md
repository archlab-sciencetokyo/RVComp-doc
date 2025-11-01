# CLINT

## Overview

The Core Local Interruptor (CLINT) is a memory-mapped device that provides inter-processor interrupt (IPI) and timer functionality in the RISC-V platform.
For details about CLINT, please refer to the [Sifive interrupt cookbook](https://sifive.cdn.prismic.io/sifive/d1984d2b-c9b9-4c91-8de0-d68a5e64fa0f_sifive-interrupt-cookbook-v1p2.pdf).
### Key Features

- **Timer**: 64-bit real-time counter (MTIME register)
- **Timer Interrupt**: Interrupt generation by timer comparison (MTIMECMP register)
- **Inter-Processor Interrupt**: IPI (Inter-Processor Interrupt) (MSIP register)
- **Address Range**: 0x02000000 - 0x020C0000


## CLINT (clint/clint.v)

CLINT is a memory-mapped device that provides inter-processor interrupt (IPI) and timer functionality in the RISC-V platform. Inter-processor interrupt and timer functionality are required by OSes, bootloaders, and firmware.

Three types of registers are defined in CLINT. The first is the MTIME register, which stores the cycle count at a certain operating frequency. The second is the MTIMECMP register, which stores the threshold of the MTIME register that triggers a timer interrupt. When the MTIME register value becomes greater than or equal to the MTIMECMP register value, a timer interrupt request is notified to the processor. The third is the MSIP register, which provides Machine-level inter-processor interrupt functionality. When 1 is written to the least significant bit of the MSIP register, an inter-processor interrupt request is notified to the processor. The upper 31 bits of the MSIP register are wired to 0.

## Register Map

| Offset | Register Name | Width | R/W | Description |
|--------|---------------|-------|-----|-------------|
| 0x2000_0000 | MSIP0 | 4B | R/W | Machine-level IPI for hart 0 |
| 0x2000_0004 | MSIP1 | 4B | R/W | Machine-level IPI for hart 1 |
| ... | ... | ... | ... | ... |
| 0x2000_3FFC | Reserved | 4B | R/W | |
| 0x2000_4000 | MTIMECMP0 | 8B | R/W | Machine-level time compare for hart 0 |
| 0x2000_4008 | MTIMECMP1 | 8B | R/W | Machine-level time compare for hart 1 |
| ... | ... | ... | ... | ... |
| 0x2000_BFF0 | MTIMECMP4094 | 8B | R/W | Machine-level time compare for hart 4094 |
| 0x0200_BFF8 | MTIME | 8B | R/W | Machine-level time counter |
