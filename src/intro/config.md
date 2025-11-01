# How to Change Configuration

When you want to change configuration in the RVComp project, multiple files may need to be updated.
We provide a script called `setting.py` that allows configuration changes while maintaining consistency. Files directly related are shown below.
This section explains the role and usage of each configuration file.

## Configuration System Overview

```
setting.py
    ↓
    ├→ src/config.vh (hardware parameters)
    └→ bootrom/rvcom.dts (device tree)
    └→ Makefile (some options)
```

## setting.py
Please grant execution permission with ```$ chmod +x setting.py ``` and execute it from the command line.
```bash
$ ./setting.py -h
```
to check available options. Please run the script with the arguments below to apply specific settings.
Available options are as follows:
| Option                        | Description                              |
|:------------------------------|:-----------------------------------------|
| -h, --help                    | Display help message                     |
| --board BOARD                 | FPGA board name (nexys4ddr, arty_a7)     |
| --clk-freq CLK_FREQ           | Clock frequency [MHz]                    |
| --l0-icache-size L0_ICACHE_SIZE | L0 instruction cache size [byte]       |
| --l1-icache-size L1_ICACHE_SIZE | L1 instruction cache size [byte]       |
| --l1-dcache-size L1_DCACHE_SIZE | L1 data cache size [byte]              |
| --l2-cache-size L2_CACHE_SIZE   | L2 cache size [byte]                   |
| --uart-baudrate UART_BAUDRATE   | UART baud rate                         |
| --itlb-entry ITLB_ENTRY         | ITLB entry count                       |
| --dtlb-entry DTLB_ENTRY         | DTLB entry count                       |
| --pht-entry PHT_ENTRY           | PHT entry count                        |
| --btb-entry BTB_ENTRY           | BTB entry count                        |

Below we explain each file that setting.py updates.
### src/config.vh - Hardware Parameters

`src/config.vh` defines modifiable hardware parameters used during RTL synthesis.

| Parameter Name   | Description                                              |
|:-----------------|:---------------------------------------------------------|
| DDR2             | Enabled when using Nexys 4 DDR board. Commented out for Arty A7 |
| CLK_FREQ_MHZ     | System clock frequency (in MHz)                          |
| PHT_ENTRIES      | Number of pattern history table entries                  |
| BTB_ENTRIES      | Number of branch target buffer entries                   |
| L0_ICACHE_SIZE   | L0 instruction cache size (in bytes)                     |
| L1_ICACHE_SIZE   | L1 instruction cache size (in bytes)                     |
| L1_DCACHE_SIZE   | L1 data cache size (in bytes)                            |
| L2_CACHE_SIZE    | L2 unified cache size (in bytes)                         |
| ITLB_ENTRIES     | Number of instruction TLB entries                        |
| DTLB_ENTRIES     | Number of data TLB entries                               |
| BAUD_RATE        | UART baud rate                                           |
| DETECT_COUNT     | Number of samples used for UART start bit detection + 1  |
| FIFO_DEPTH       | UART transmit/receive FIFO size (in bytes)               |

### src/rvcom.dts - Device Tree
In memory settings, please specify a DRAM size of 128 MiB for the Nexys 4 DDR board and 256 MiB for the Arty A7 board.
Please set the clock frequency in Hz in the clock-frequency field.

### Makefile - Some Options
Please set `BAUD_RATE` to match the UART baud rate.
