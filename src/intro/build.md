# Linux Build

This section explains how to build a Linux system for RVComp using [RVComp-buildenv](https://github.com/archlab-sciencetokyo/RVComp-buildenv).

The following tools are required. Please refer to the [Installation Guide](install.md).

- riscv-gnu-toolchain
- Device Tree Compiler

Buildroot is included as a submodule in RVComp-buildenv and does not need to be installed separately.



We have verified Linux kernel version 6.19.5.

## RVComp-buildenv

[RVComp-buildenv](https://github.com/archlab-sciencetokyo/RVComp-buildenv) is a standalone build environment for Linux images for RVComp. It bundles Buildroot as a submodule and provides `command.sh`, which automates the configure and build steps.

### Getting the Source

```bash
$ git clone https://github.com/archlab-sciencetokyo/RVComp-buildenv.git
$ cd RVComp-buildenv
$ git submodule update --init --recursive
```

### Building

Before building, unset any compiler include-path variables that may interfere with cross-compilation:

```bash
$ unset CPATH
$ unset C_INCLUDE_PATH
$ unset CPLUS_INCLUDE_PATH
```

Run `command.sh` with the boot method and the path to the RVComp Buildroot external tree.
`BR2_EXTERNAL` is Buildroot's mechanism for providing external packages and defconfigs outside the Buildroot source tree; pass the `RVComp/buildroot/` directory here.
The defconfigs (`uart_defconfig`, `mmc_defconfig`) specify the Linux kernel version, kernel configuration, package selection, and root filesystem format for each boot method.

```
Usage: ./command.sh <uart|mmc> <br2_external>

  uart  build uart_defconfig
  mmc   build mmc_defconfig
```

**UART boot:**

```bash
$ ./command.sh uart /path/to/RVComp/buildroot
```

**MMC boot:**

```bash
$ ./command.sh mmc /path/to/RVComp/buildroot
```

### Output

The build output is placed under `images/`:

- `images/uart/fw_payload.bin`: Linux payload for UART boot
- `images/mmc/fw_payload.bin`: Combined image (`fw_payload.bin` padded to 32 MiB followed by `rootfs.ext4`), ready to write to a microSD card

**UART boot:**

Copy `fw_payload.bin` to `RVComp/image/`, then rebuild the bitstream:

```bash
$ cp images/uart/fw_payload.bin /path/to/RVComp/image/fw_payload.bin
$ cd /path/to/RVComp
$ make bit
```

Update `BIN_SIZE` in `config.mk` with the actual file size before running `make bit`:

```bash
$ stat images/uart/fw_payload.bin   # read the Size: field
```

**MMC boot:**

Write the combined image to a microSD card, set `BIN_SIZE` to 32 MiB in `config.mk`, then rebuild the bitstream:

```bash
$ sudo dd if=images/mmc/fw_payload.bin of=/dev/sdX bs=1M conv=fsync,notrunc status=progress
$ cd /path/to/RVComp
$ make bit
```

Set `BIN_SIZE = 33554432` (32 MiB) in `config.mk` before running `make bit`. See [Setup Before Make Command](makesetup.md) for details.

## Kernel Modules and Boot Files

For details on the RVComp-specific kernel modules (`rvcomp-ethernet`, `rvcomp-mmc`) and boot scripts (`rvcomp-bootfiles`) included in the Buildroot packages, see [Device Drivers](../software/drivers.md).


