# Memory Mapped Region

This section explains the memory map and Memory-Mapped I/O (MMIO) of the RVComp system. RVComp has a 34-bit physical address space, with memory and peripherals mapped to specific address ranges.

## Memory Map Overview

RVComp's physical memory map is configured as follows:

| **Start**         | **End**           | **Device/Region**      |
|:-----------------:|:-----------------:|:----------------------:|
| 0x0001_0000       | 0x0001_1FFF       | bootrom                |
| 0x0200_0000       | 0x020B_FFFF       | CLINT                  |
| 0x0C00_0000       | 0x0CFF_FFFF       | PLIC                   |
| 0x1000_0000       | 0x1000_000F       | UART                   |
| 0x1000_0100       | 0x1000_0103       | Soft reset             |
| 0x1400_0000       | 0x1400_3FFF       | Ethernet MAC CSRs      |
| 0x1800_0000       | 0x18XX_XXXX       | Ethernet RX buffer     |
| 0x1C00_0000       | 0x1CXX_XXXX       | Ethernet TX buffer     |
| 0x8000_0000       | 0x87FF_FFFF       | DRAM (Nexys4DDR)       |
| 0x8000_0000       | 0x8FFF_FFFF       | DRAM (ArtyA7)          |
| 0xA000_0000       | 0xA000_1FFF       | sdcram (CSRs + 4 KiB window) |

:::{note}
The Ethernet RX and TX buffer end addresses (`0x18XX_XXXX` / `0x1CXX_XXXX`) are variable — their sizes are determined at synthesis time by the `ETHER_RXBUF_SIZE` and `ETHER_TXBUF_SIZE` parameters in `src/config.vh`. `axi_interconnect.v` uses broad address decoding and is not updated every time buffer sizes change, so accesses to addresses beyond the configured buffer size may not raise an exception. To enforce strict address checking, `axi_interconnect.v` must be edited manually. See [Ethernet Architecture](../arch/ethernet.md) for the full CSR map.
:::

For details on each item, please refer to [SoC Architecture](../arch/index.md).

## Soft Reset Register

The soft reset register at `0x1000_0100` allows software to perform a system-wide reset without power-cycling the FPGA board. Writing any value to this 32-bit register asserts the reset signal across the entire SoC, including the CPU, caches, and all peripherals. The FPGA bitstream is not reloaded; only the on-chip logic is reset. This is primarily useful during development to re-run the boot sequence quickly.

:::{note}
DRAM itself is not included in the soft reset domain. Routing the reset signal to the DRAM controller raises wiring and stability concerns, so DRAM contents are preserved across a soft reset. Software should not rely on DRAM being in a clean state after reset.
:::
