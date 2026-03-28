# Software

This section describes the software stack that accompanies the RVComp hardware.

## [Buildroot and BR2_EXTERNAL](buildroot.md)

RVComp uses Buildroot to build the Linux kernel, OpenSBI, and root filesystem. The `RVComp/buildroot/` directory is a BR2_EXTERNAL tree that provides defconfigs, kernel configs, custom packages, and overlay files outside the Buildroot source tree.

## [Linux Boot Flow](boot-flow.md)

Describes the boot sequence from reset through to userspace for both UART boot and MMC boot, including the early-boot hooks that load drivers and mount the root filesystem.

## [RVComp Device Drivers](drivers.md)

Documents the out-of-tree Linux drivers for the RVComp-specific hardware: `rvcomp-ethernet` for the Ethernet controller and `rvcomp-mmc` for the sdcram-backed block device.
