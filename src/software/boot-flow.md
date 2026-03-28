# Linux Boot Flow

## Overview

RVComp uses `fw_payload.bin` as the software payload in both supported boot modes. The exact boot path depends on which bootrom mode was selected when the bitstream was built and which Buildroot configuration was used to generate the Linux image.

The two Buildroot configurations are:

- `uart_defconfig`: builds a system that runs entirely from an initramfs in RAM
- `mmc_defconfig`: builds the same payload plus a persistent `rootfs.ext4` for MMC boot on Nexys 4 DDR

## UART Boot

1. The bootrom starts in UART boot mode and waits for the payload.
2. The host-side serial tool sends `fw_payload.bin` over UART.
3. The bootrom copies the received payload into DRAM and jumps to it.
4. OpenSBI starts first, then hands control to the Linux kernel.
5. Linux boots and mounts the initramfs embedded in `fw_payload.bin` as the root filesystem.
6. The `S20-rvcomp-ethernet` hook runs `modprobe rvcomp_ethernet` to load the Ethernet driver.

## MMC Boot

1. `fw_payload.bin` is written at offset 0 of the microSD card; `rootfs.ext4` follows at the 32 MiB offset.
2. At power-on, the bootrom copies `fw_payload.bin` from the sdcram MMIO window into DRAM.
3. OpenSBI starts, then launches the Linux kernel.
4. The minimal initramfs inside `fw_payload.bin` starts first.
5. The `S20-rvcomp-ethernet` hook runs `modprobe rvcomp_ethernet` to load the Ethernet driver.
6. The `S30-rvcomp-mmc-rootfs` hook loads `rvcomp_mmc`, waits for `/dev/mmcblk0`, mounts the ext4 filesystem, and performs `switch_root`.

Because the `rvcomp-mmc` driver applies `rootfs-offset` from the device tree, Linux accesses the root filesystem directly via `/dev/mmcblk0` without a partition table.

## Early-Boot Hooks

The hooks under `/etc/rvcomp/initramfs.d/` are sourced in alphanumeric order by `/init`.

### S20-rvcomp-ethernet

Loads the Ethernet driver:

```sh
modprobe rvcomp_ethernet
```

The network interface is brought up but has no IP address by default. To configure the network at boot, add the following lines to `S20-rvcomp-ethernet`:

```sh
ip addr add <IP_ADDRESS>/<PREFIX_LEN> dev eth0
ip link set eth0 up
```

### S30-rvcomp-mmc-rootfs

Used in MMC boot only. Loads the block driver, waits for `/dev/mmcblk0` to appear, mounts the ext4 root filesystem, and performs `switch_root` to hand off to the persistent userspace.

## Filesystem Modes

### Initramfs-only (UART boot)

`uart_defconfig` embeds the root filesystem into `fw_payload.bin`. Easy to boot, but filesystem changes are lost on reset or power-off.

### Persistent root filesystem (MMC boot)

`mmc_defconfig` produces both the boot payload and a separate ext4 filesystem. Early userspace transitions from the initramfs to the persistent filesystem during boot via `switch_root`.

## Patches

### BusyBox syslogd — `ctime` null pointer fix

BusyBox's syslogd calls `ctime()` from glibc to format log timestamps. On RVComp, `ctime()` can return a null pointer, causing a null pointer exception. A patch is applied to BusyBox to work around this.

The patch is located at `RVComp/buildroot/patches/busybox/0001-sysklogd-use-local-timestamp-buffer.patch`.

**What the patch does:**

The patch adds a `format_local_timestamp()` function and replaces all `ctime()` calls in `sysklogd/syslogd.c` with it. The new function:

1. Calls `localtime_r()` instead of `ctime()` and validates its return value and all fields (`tm_mon`, `tm_mday`, `tm_hour`, `tm_min`, `tm_sec`).
2. Falls back to `"Jan  1 00:00:00"` if `localtime_r()` returns NULL or produces an out-of-range value.
3. Writes the formatted timestamp into a local stack buffer (`char timestamp_buf[20]`) instead of using the static buffer returned by `ctime()`.

This eliminates the null pointer dereference and makes timestamp formatting safe.
