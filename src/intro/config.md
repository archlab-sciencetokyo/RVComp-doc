# How to Change Configuration



When you want to change hardware configuration in the RVComp project, several generated files must stay in sync. RVComp provides two front ends for this task: `make menuconfig` for an interactive terminal UI and `make cliconfig` for scripted changes.

## Configuration System Overview

Both front ends are implemented by `RVComp/tools/setting.py`. They do **not** generate a `.config` file or use Kconfig. Instead, they read the current settings from the repository and then update the relevant source files directly.

```
make menuconfig
    └─> uv run --project tools/ setting

make cliconfig ARGS="..."
    └─> uv run --project tools/ cliconfig ...

Updated files
    ├→ src/config.vh
    ├→ bootrom/rvcomp.dts
    ├→ bootrom/src/rvcomp_ether.h
    ├→ config.mk
    ├→ Makefile          # BAUD_RATE only
    └→ bootrom/src/bootloader.c
```

The last file is used to switch the bootrom between UART boot and MMC boot at compile time.

## make menuconfig

```bash
$ make menuconfig
```

This target launches the curses-based configuration UI provided by `tools/setting.py`. The interface is menuconfig-style, but it is a standalone RVComp utility rather than the Linux Kconfig system.

```{raw} html
<div style="text-align: center">
  <img src="../_static/media/menuconfig_gui.png" alt="menuconfig GUI" style="max-width: 100%">
</div>
```

**Navigation:**

- **Up / Down arrow**: Move between items
- **Enter**: Select or toggle the highlighted item
- **Left / Right arrow**: Switch between the bottom buttons (`Save`, `Load Default`, `Exit`)

The top-level sections are:

| Menu section              | Parameters covered                                        |
|:--------------------------|:----------------------------------------------------------|
| Board                     | Target FPGA board (`nexys4ddr` / `arty_a7`)               |
| Boot Method               | UART boot or MMC boot (`nexys4ddr` only)                  |
| CPU / Branch Predictor    | Clock frequency, PHT entries, BTB entries                 |
| Cache                     | L0/L1/L2 cache sizes                                      |
| TLB                       | ITLB / DTLB entry counts                                  |
| UART                      | Baud rate and FIFO depth                                  |
| Ethernet                  | RX/TX buffer sizes                                        |

When you save the configuration, the tool writes the updated values back to the source files listed above.

After changing the configuration, regenerate the bitstream:

```bash
$ make reclockbit    # if you changed the clock frequency
$ make rebit         # for other configuration changes
```

## make cliconfig

```bash
$ make cliconfig ARGS="--board arty_a7 --clk-freq 150"
```

This target runs the non-interactive CLI entry point in the same tool. It is intended for scripts and for cases where you already know the exact values you want to set.

```
usage: cliconfig [-h] [--board {nexys4ddr,arty_a7}] [--boot {mmc,uart}] [--default] [--clk-freq MHz] [--pht-entry N]
                 [--btb-entry N] [--l0-icache-size bytes] [--l1-icache-size bytes] [--l1-dcache-size bytes]
                 [--l2-cache-size bytes] [--itlb-entry N] [--dtlb-entry N] [--baudrate bps] [--fifo-depth N]

RVComp CLI configuration tool

Available boards: nexys4ddr, arty_a7

options:
  -h, --help            show this help message and exit
  --board {nexys4ddr,arty_a7}
                        FPGA board
  --boot {mmc,uart}     Boot method
  --default             Load board defaults (requires --board)
  --clk-freq MHz
  --pht-entry N
  --btb-entry N
  --l0-icache-size bytes
  --l1-icache-size bytes
  --l1-dcache-size bytes
  --l2-cache-size bytes
  --itlb-entry N
  --dtlb-entry N
  --baudrate bps
  --fifo-depth N
```

Examples:

```bash
# Change the target board to Arty A7 with MMC boot
$ make cliconfig ARGS="--board arty_a7"

# Change multiple settings at once
$ make cliconfig ARGS="--board nexys4ddr --clk-freq 160 --baudrate 3200000"
```

## Updated Files

### src/config.vh - Hardware Parameters

`src/config.vh` defines the RTL parameters used during synthesis, including board selection, cache sizes, TLB entry counts, UART settings, and Ethernet buffer sizes.

### bootrom/rvcomp.dts - Device Tree

`bootrom/rvcomp.dts` is updated to keep the clock frequency, DRAM size, and peripheral address ranges consistent with the selected board and Ethernet buffer configuration.

### bootrom/src/rvcomp_ether.h - Bare-Metal Ethernet Constants

`bootrom/src/rvcomp_ether.h` mirrors the Ethernet RX/TX buffer sizes for the bootrom-side software helpers.

### config.mk / Makefile

`config.mk` is updated with board selection and `BAUD_RATE`. `Makefile` is also updated so the serial communication targets use the same UART baud rate.

### bootrom/src/bootloader.c

The tool comments or uncomments `#define UART_BOOT` in `bootloader.c` so that the bootrom build matches the selected boot method.

## Board Default Values

| Parameter            | Nexys 4 DDR | Arty A7  |
|:---------------------|------------:|---------:|
| Clock Frequency      | 150 MHz     | 150 MHz  |
| PHT Entries          | 8192        | 8192     |
| BTB Entries          | 512         | 512      |
| L0 ICache Size       | 1 KiB       | 1 KiB    |
| L1 ICache Size       | 16 KiB      | 16 KiB   |
| L1 DCache Size       | 16 KiB      | 16 KiB   |
| L2 Cache Size        | 128 KiB     | 64 KiB   |
| ITLB Entries         | 128         | 128      |
| DTLB Entries         | 128         | 128      |
| UART Baud Rate       | 3,000,000   | 3,000,000|
| UART FIFO Depth      | 2048        | 2048     |
| Ethernet RX Buffer   | 16 KiB      | 16 KiB   |
| Ethernet TX Buffer   | 8 KiB       | 4 KiB    |

