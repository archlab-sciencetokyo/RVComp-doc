# AXI-based Interconnect

## Overview

The AXI-based interconnect is a module that performs bus arbitration between the CPU and each peripheral. It uses an AXI4-Lite based protocol. It realizes address decoding and routing through memory-mapped I/O.

The differences from AXI4-Lite are the following two points:
- wvalid/awvalid and wready/awready are unified (handshake of w channel and aw channel is not independent)
- dram and bootrom have 128-bit data width (not 32-bit width)


### Key Functions

- **Protocol**: AXI4-Lite compliant
- **Master**: L2 Cache (via CPU/MMU)
- **Slaves**: Boot ROM, CLINT, PLIC, UART, DRAM
- **Arbitration**: Single master, multiple slaves
- **Address Decode**: Automatic routing based on memory map

## Memory Map
Sends and receives data with appropriate modules based on addresses.

| **Address Range**               | **Device/Region**      |
|:-------------------------------:|:----------------------:|
| 0x0001_0000 - 0x0001_1FFF        | bootrom                |
| 0x0200_0000 - 0x020B_FFFF        | CLINT                  |
| 0x0C00_0000 - 0x0CFF_FFFF        | PLIC                   |
| 0x1000_0000 - 0x1000_00FF        | UART                   |
| 0x8000_0000 - 0x87FF_FFFF        | DRAM (Nexys4DDR)       |
| 0x8000_0000 - 0x8FFF_FFFF        | DRAM (ArtyA7)          |

## Architecture

```
         L2 Cache
             |
    +--------v---------+
    | AXI Interconnect |
    |  (Address Decode)|
    +--------+---------+
             |
    +--------+--------+--------+--------+--------+
    |        |        |        |        |        |
  BootROM  CLINT    PLIC     UART     DRAM
```

## Protocol
Uses AXI4-Lite based protocol.

| Signal Name | Direction | Bit Width | Description |
|--------|------|----------|------|
| `peripheral_wvalid_o` | output | 1 | Write address valid |
| `peripheral_wready_i` | input | 1 | Write address ready |
| `peripheral_awaddr_o` | output | 32 - MMIO_WIDTH | Write address |
| `peripheral_wdata_o` | output | 32 or 128 | Write data |
| `peripheral_wstrb_o` | output | 4 or 16 | Write strobe |
| `peripheral_bvalid_i` | input | 1 | Write response valid |
| `peripheral_bready_o` | output | 1 | Write response ready |
| `peripheral_bresp_i` | input | 2 | Write response status |
| `peripheral_arvalid_o` | output | 1 | Read address valid |
| `peripheral_arready_i` | input | 1 | Read address ready |
| `peripheral_araddr_o` | output | 32 - MMIO_WIDTH| Read address |
| `peripheral_rvalid_i` | input | 1 | Read data valid |
| `peripheral_rready_o` | output | 1 | Read data ready |
| `peripheral_rdata_i` | input | 32 or 128 | Read data |
| `peripheral_rresp_i` | input | 2 | Read response status |


## State Machine

| State Name | Description |
|--------|------|
| `WR_IDLE` | Idle state, wait for write request |
| `WR_CLINT` | Writing to CLINT, wait for response |
| `WR_PLIC` | Writing to PLIC, wait for response |
| `WR_UART` | Writing to UART, wait for response |
| `WR_DRAM` | Writing to DRAM, wait for response |
| `WR_RET` | Return response, send response to CPU |
