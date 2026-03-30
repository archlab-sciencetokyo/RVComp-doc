# Device Drivers

## Overview

RVComp provides two out-of-tree Linux kernel drivers as Buildroot packages. Both drivers are licensed under the GNU General Public License version 2 (GPL-2.0).

| Package | Module | Role |
|:--------|:-------|:-----|
| `rvcomp-ethernet` | `rvcomp_ethernet` | Linux network interface for the RVComp Ethernet controller |
| `rvcomp-mmc`      | `rvcomp_mmc`      | Linux block device backed by sdcram |

## rvcomp-ethernet

- **Source**: `RVComp/buildroot/package/rvcomp-ethernet/src/rvcomp_ethernet.c`
- **Module name**: `rvcomp_ethernet`
- **Device tree compatible**: `isct,rvcomp-ethernet`
- **License**: GPL-2.0

This driver exposes the RVComp Ethernet controller as a standard Linux network interface (`eth0`). It maps the CSR region and the RX/TX MMIO buffer regions at probe time.

### Receive Flow

```
PHY → [hardware: MAC filter, FCS check, write to RX buffer, advance ADDR_END]
    → driver detects ADDR_END != ADDR_START
    → allocates skb
    → reads frame bytes from RX buffer into skb
    → passes skb to Linux network stack
    → advances ADDR_START
```

### Transmit Flow

```
Linux network stack calls ndo_start_xmit
    → driver writes 32-bit frame-length header + payload into TX buffer
    → driver advances TX_BUFFER_END
    → [hardware: prepend preamble/SFD, append FCS, transmit via PHY]
```

Hardware handles destination-MAC filtering and FCS processing; the driver does not need to calculate or strip the FCS.

## rvcomp-mmc

- **Source**: `RVComp/buildroot/package/rvcomp-mmc/src/rvcomp_mmc.c`
- **Module name**: `rvcomp_mmc`
- **Device tree compatible**: `isct,rvcomp-mmc`
- **License**: GPL-2.0

This driver exposes sdcram-backed storage as the block device `/dev/mmcblk0`. It does not use the Linux MMC host framework; it is a block driver that services requests through the sdcram MMIO window.

The driver reads `rootfs-offset` from the device tree so that the block device address space starts at the root filesystem region on the card, not at offset 0.

### Read Flow

```
Linux block layer issues read request (512-byte sectors)
    → driver writes target page address (upper 29 bits) to CSR_ADDR29
    → driver reads 32-bit words through the 4 KiB MMIO window
    → copies data into the request buffer
    → completes the block request
```

### Write Flow

```
Linux block layer issues write request (512-byte sectors)
    → driver writes target page address (upper 29 bits) to CSR_ADDR29
    → driver writes through the 4 KiB MMIO window
    → completes the block request (writes buffered in write-back cache)
```

Flush is not issued on every write. It is triggered only when the block layer issues an explicit `REQ_OP_FLUSH` (e.g. on fsync or unmount):

```
Linux block layer issues flush request (REQ_OP_FLUSH)
    → driver writes 1 to CSR_FLUSH
    → driver polls CSR_FLUSH_DONE until flush completes
    → driver clears FLUSH_DONE latch (CSR_FLUSH_DONE_CLR)
    → completes the flush request
```

## In-Kernel Support

PLIC, CLINT, and the serial console are handled by standard in-kernel drivers configured through the RVComp kernel defconfig. No out-of-tree modules are required for these peripherals.
