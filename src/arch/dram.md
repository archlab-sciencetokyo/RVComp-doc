# DRAM Controller

## Overview

The DRAM controller is a module that provides an interface to DDR2/DDR3 SDRAM using MIG (Memory Interface Generator) IP provided by AMD. It handles data transfer between different clocks and connects the DRAM controller with the interconnect.
The MIG GUI setup method is described in [MIG setup](../intro/ipguisetup.md).

```
dram_controller (dram/dram_controller.v)   # DRAM controller
├── async_fifo (dram/async_fifo.v)         # Asynchronous FIFO
├── synchronizer (synchronizer.v) ×3       # Clock domain synchronization
└── mig_7series_0 (Xilinx IP)              # MIG DDR2/DDR3 controller
```

### Key Features

- **Supported Memory**: DDR2 / DDR3 SDRAM
- **IP**: Uses Xilinx Memory Interface Generator for DRAM controller.
- **Address Range**: 0x80000000 - 0x90000000 (Nexys)
                   0x80000000 - 0xa0000000 (Arty)
- **Data Width**: 128-bit


### async_fifo (dram/async_fifo.v)
The asynchronous FIFO is a FIFO buffer for safely transferring data between different clock domains.
It transfers data between the system clock domain and the DRAM clock domain.
The FIFO depth is 512 entries with 128-bit width.

### synchronizer (synchronizer.v)
Clock domain synchronization circuit using 2-stage flip-flops.
Used for synchronization of initialization and reset signals.

### mig_7series_0 (Xilinx IP)
MIG provided by AMD is an IP core for controlling DDR2/DDR3 SDRAM on FPGA.
It performs complex DRAM control such as row selection, column selection, bank selection, refresh, and timing control.
For details, refer to [AMD's Memory Interface Documentation](https://www.amd.com/en/products/adaptive-socs-and-fpgas/intellectual-property/mig.html).
The MIG GUI setup method is described in [MIG setup](../intro/ipguisetup.md).

