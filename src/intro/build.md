# Linux Build

This section explains how to build a Linux system for RVComp. Using Buildroot, we generate the Linux kernel and root filesystem.
The following tools and software are required.
Please refer to the [Installation Guide](install.md).
- riscv-gnu-toolchain
- Buildroot
- OpenSBI (modified for RVComp)
- Device Tree Compiler

If you want to use the latest Linux kernel, download the latest Linux kernel.

## Building with Buildroot
Buildroot is a tool that can easily build embedded Linux systems. Buildroot configuration files for RVComp are included in the RVComp repository.
### Setting Environment Variables
If you do not set environment variables as follows before building, the build may fail.
```bash
$ unset CPATH
$ unset C_INCLUDE_PATH
$ unset CPLUS_INCLUDE_PATH
```

Replace \<install dir\> with the path to the directory where RVComp is installed (either relative or absolute path).
```bash
$ git clone https://github.com/buildroot/buildroot.git
$ cd buildroot
$ git checkout 2025.02
$ make BR2_EXTERNAL=<install dir>/rvcomp/buildroot/ uart_defconfig
$ make
```
Before executing `make`, you can select Linux kernel version and additional packages with `make menuconfig`. For details, refer to the [Buildroot documentation](https://buildroot.org/downloads/manual/manual.html).


If the build succeeds, the following files are generated in the `output/images/` directory:
- `rootfs.cpio`: Root filesystem
- `Image`: Linux kernel image
- `fw_payload.elf`: OpenSBI ELF file
- `fw_payload.bin`: OpenSBI image
fw_payload.bin is an image containing initramfs + Linux + OpenSBI.
When booting Linux on RVComp, this file is sent.

By copying `output/images/fw_payload.bin` to `rvcomp/images`, it becomes possible to perform Linux boot simulation with `make linux`.

Also, when booting Linux on FPGA, the first bootloader needs to recognize the size of fw_payload.bin, so check the size with the following command:
```bash
$ stat fw_payload.bin
```
Set the Size: value in `BIN_SIZE` in config.mk.

