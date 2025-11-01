# PLIC

## Overview

The PLIC (Platform-Level Interrupt Controller) is the external interrupt controller in RISC-V. The specification is [here](https://github.com/riscv/riscv-plic-spec).

### Key Features

- **Interrupt Sources**: Up to 128 (current implementation: 2)
- **Priority Levels**: 0-15 (0=interrupt disabled)
- **Contexts**: 2 (M-mode, S-mode)
- **Arbitration**: Priority-based automatic selection
- **Protocol**: AXI4-Lite
- **Address Range**: 0x0C000000 - 0x0D000000


### PLIC (plic/plic.v)

PLIC is the external interrupt controller in the RISC-V platform. PLIC consists of PLIC Gateways and PLIC Core. Interrupt requests from interrupt sources are conveyed from PLIC Gateways to PLIC Core, and the interrupt request with the highest priority is selected and notified for each interrupt target.

PLIC Gateways convert interrupt requests from interrupt sources into a common format and control the interrupt request flow to PLIC Core. PLIC Gateways ensure that there is at most one interrupt request to PLIC Core per interrupt source. A PLIC Gateway does not notify new interrupt requests to PLIC Core until it receives notification that interrupt handler processing is complete.

PLIC Core receives interrupt requests from PLIC Gateways and notifies the processor when the interrupt with the highest priority exceeds the threshold. PLIC allows setting priority and threshold per interrupt source and disabling interrupts.

When the processor receives an interrupt request from PLIC, it transfers control to the interrupt handler. The interrupt handler reads the PLIC's Interrupt Claim register to obtain the Interrupt ID and determines the interrupt source to perform corresponding processing. The mapping between Interrupt ID and interrupt source is described in the Devicetree. When the Interrupt Claim register is read, the Interrupt Pending Bit of the interrupt source with the highest priority is cleared.

The processor writes the Interrupt ID to the Interrupt Completion register to notify PLIC that interrupt handler processing is complete. After receiving that notification, PLIC Gateways can notify new interrupt requests from corresponding interrupt sources to PLIC Core.


<!-- TODO: Add diagram -->

