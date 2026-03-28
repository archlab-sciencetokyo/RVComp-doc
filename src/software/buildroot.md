# Buildroot and BR2_EXTERNAL

## BR2_EXTERNAL

Buildroot supports an external tree mechanism called `BR2_EXTERNAL`. It allows project-specific defconfigs, kernel configs, packages, and overlay files to live outside the Buildroot source tree. RVComp uses this mechanism: `RVComp/buildroot/` is the BR2_EXTERNAL tree.

When invoking `make`, the `BR2_EXTERNAL` variable is set to point at `RVComp/buildroot/`, making the defconfigs and packages in that tree visible to Buildroot.

## Build Flow

### UART Boot

`uart_defconfig` produces a single `fw_payload.bin` that bundles OpenSBI, the Linux kernel, and an initramfs. The system runs entirely from RAM.

```
uart_defconfig
└── fw_payload.bin  (OpenSBI + Linux kernel + initramfs)
```

### MMC Boot

MMC boot requires two separate outputs. Because the payload and the root filesystem include different packages, they are built in two separate passes. Using the same base configuration (`mmc_defconfig`) for both passes avoids dependency and library version differences between the two builds.

**First pass** — payload:

```
mmc_defconfig
└── fw_payload.bin  (OpenSBI + Linux kernel + minimal initramfs)
```

**Second pass** — root filesystem:

```
mmc_defconfig + mmc_rootfs_second_pass.fragment
└── rootfs.ext4  (ext4, 64 MiB)
```

`mmc_rootfs_second_pass.fragment` is applied on top of `mmc_defconfig`. The fragment overrides only the differences: disabling the kernel and OpenSBI builds, switching the root filesystem format to ext4, and adding packages such as dropbear and curl.

## Disk Layout

By default, the MMC boot disk image has the following layout:

```
Offset 0          Offset 32 MiB               Offset 96 MiB
│                 │                            │
▼                 ▼                            ▼
┌─────────────────┬────────────────────────────┐
│  fw_payload.bin │       rootfs.ext4          │
│    (32 MiB)     │         (64 MiB)           │
└─────────────────┴────────────────────────────┘
```

`fw_payload.bin` is padded to 32 MiB so that `rootfs.ext4` always starts at a fixed offset. The `rvcomp-mmc` driver reads `rootfs-offset` from the device tree to know where the root filesystem begins.

### Adding Packages to the Root Filesystem

To add packages to `rootfs.ext4`, add `BR2_PACKAGE_*` options to `mmc_rootfs_second_pass.fragment`. Only the differences from `mmc_defconfig` need to be listed in the fragment.

Adding packages increases the required rootfs size. Update `BR2_TARGET_ROOTFS_EXT2_SIZE` in `mmc_rootfs_second_pass.fragment` accordingly and rebuild.

### Changing the 32 MiB Offset

If you need to change the offset, update both of the following and rebuild the bitstream:

- `bootrom/rvcomp.dts` — `rootfs-offset` property (byte offset as a 64-bit value)
- `config.mk` — `BIN_SIZE` (set to the new offset in bytes; `33554432` for 32 MiB)
