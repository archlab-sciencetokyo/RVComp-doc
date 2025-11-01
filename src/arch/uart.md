# UART Controller

## Overview

The UART controller is a peripheral that realizes serial communication (RS-232). It supports transmit/receive FIFOs, baud rate generation, and asynchronous communication protocol, enabling communication with external devices and PCs.

## Module Hierarchy

```
uart (uart/uart.v)
├── fifo × 2 (uart/fifo.v)                 # FIFO buffer
├── uart_rx (uart/uart_rx.v)               # UART receiver
│   └── synchronizer (synchronizer.v)      # Clock domain synchronization
└── uart_tx (uart/uart_tx.v)               # UART transmitter
```

### Key Features

- **Baud Rate**: Configurable
- **FIFO**: Transmit/receive buffers
- **Interface**: AXI4-Lite based interconnect

### Submodule Description

#### fifo (uart/fifo.v)
FIFO for transmit/receive buffers. Has configurable depth and is instantiated twice as transmit FIFO (TX buffer) and receive FIFO (RX buffer). Implemented in BRAM, uses 2048 entries to utilize the minimum BRAM capacity as much as possible.

#### synchronizer (synchronizer.v)
Clock domain synchronization circuit using 2-stage flip-flops.
Used for synchronization of the rxd signal.

#### uart_rx (uart/uart_rx.v)
UART receive module.
Detects start bit and performs sampling at the center of the signal.
Our UART receive module does not handle errors very well.

#### uart_tx (uart/uart_tx.v)
UART transmit module.
Transmits start bit, 8-bit data, and stop bit after waiting for the number of cycles according to the baud rate.




## State Machine

### uart.v (Top-level Control)

#### Read State Machine

| State | Operation |
|-------|------|
| `RD_IDLE` | Wait for read request |
| `RD_WAIT` | Wait for data read from RXFIFO |

#### Write State Machine

| State | Operation |
|-------|------|
| `WR_IDLE` | Wait for write request |
| `WR_WAIT` | Wait for data write to TXFIFO |

### uart_tx.v (Transmitter Control)

| State | Operation |
|-------|------|
| `IDLE` | Wait for transmit request, txd=1 (HIGH) |
| `RUN` | Transmitting data (start bit→8 data bits→stop bit) |

### uart_rx.v (Receiver Control)

| State | Operation |
|-------|------|
| `IDLE` | Wait for start bit detection |
| `RUN` | Receiving data (start bit verification→8 data bit reception→stop bit verification) |
