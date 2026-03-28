# sdcram

## Overview

sdcram is a wrapper that allows software to access storage like RAM. It includes an on-chip write-back cache implemented in FPGA block RAM. The storage interface runs at 25 MHz (50 MHz system clock divided by 2).

The controller is mapped at `0xA000_0000`. Software programs a 29-bit address selector in the CSR region and then accesses data through the 4 KiB window at `0xA000_1000`-`0xA000_1FFF`.

Linux conventionally uses the name `mmc` for storage-related software components; in this context, `mmc` refers to software that controls this module.

## Module Hierarchy

```text
sdcram_controller (sdcram/sdcram_controller.v)       # AXI wrapper, CSR handling, window logic
└── sdcram (sdcram/sdcram.v)                         # Cache and storage access core
    ├── sdcram_interface (sdcram/sdcram_interface.v)     # Interface
    │   └── sdcram_protocol (sdcram/sdcram_protocol.v)   # Command/data state machine
    │       ├── sdcram_dat_transceiver (sdcram/sdcram_dat_transceiver.v)
    │       │   └── sdcram_crc_16 (sdcram/sdcram_crc_16.v) ×4
    │       └── sdcram_cmd_transceiver (sdcram/sdcram_cmd_transceiver.v)
    │           ├── cmd_rom (sdcram/cmd_rom.v)
    │           └── sdcram_crc_7 (sdcram/sdcram_crc_7.v)
    ├── cache_tags (sdcram/cache_tags.v)
    └── tdp_rf_bw2clk (sdcram/tdp_rf_bw2clk.v)
```

## CSR Map

The sdcram MMIO region starts at `0xA000_0000`. It is divided into a control register area and a 4 KiB data window.

### Control Registers

| Address        | Name                 | Access | Description |
|:--------------:|:---------------------|:------:|:------------|
| 0xA000_0000    | `CSR_ADDR29`         | R/W    | Upper 29 bits of the byte address mapped into the window |
| 0xA000_0018    | `CSR_FLUSH`          | W      | Triggers a flush of dirty cache lines |
| 0xA000_001C    | `CSR_FLUSH_DONE`     | R      | Sticky completion flag for the flush operation |
| 0xA000_0020    | `CSR_FLUSH_DONE_CLR` | W1C    | Clears `CSR_FLUSH_DONE` |

### Data Window

The 4 KiB data window occupies `0xA000_1000`-`0xA000_1FFF`.

- Reads return data from the cache when available
- Cache misses fetch data from the backing storage
- Writes update the cache and are written back later

## Cache

- **Size**: 8 KiB (FPGA block RAM)
- **Write policy**: write-back

## Address Space

The backing storage address space is 41 bits wide. Software selects a 4 KiB region within this space by writing the upper 29 bits to `CSR_ADDR29`. The lower 12 bits (4 KiB offset) are then used directly when accessing the window.

## CPU Access

1. Write the upper 29 bits of the target byte address to `CSR_ADDR29`
2. Read or write 32-bit values through the 4 KiB MMIO window at `0xA000_1000`–`0xA000_1FFF`

## Software Support

For the Linux block driver and bare-metal helpers, see [Device Drivers](../software/drivers.md).

## External Pins

The sdcram block connects to the MicroSD slot on the Nexys 4 DDR board. Exact pin assignments are defined in `constr/Nexys-A7-100T-Master.xdc`.

| Signal        | Direction | Description |
|:--------------|:----------|:------------|
| `sd_sclk`     | Output    | SD clock |
| `sd_cmd`      | Inout     | SD command line |
| `sd_dat[3:0]` | Inout     | SD data lines |
| `sd_rst`      | Output    | SD card reset |
| `sd_cd`       | Input     | Card-detect input |


