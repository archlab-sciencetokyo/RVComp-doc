# Installation Guide

This section explains how to install the required tools.

If you are on Windows, begin with [Setup Git and Make on Windows](#setup-git-and-make-on-windows) to install the `git` and `make` commands. Please run [RVComp install](#rvcomp-install) first, then install the remaining tools.

The following tools are required for logic synthesis and place-and-route:

- [device-tree-compiler](#device-tree-compiler)
- [riscv-gnu-toolchain](#riscv-gnu-toolchain)
- [Vivado](#vivado)
- [Xilinx Board Files](#xilinx-board-files)

The simulation flow requires:

- [riscv-gnu-toolchain](#riscv-gnu-toolchain)
- [Verilator](#verilator)

To use the serial communication utility we provide for the FPGA boards, install:

- [uv](#uv)

On Windows you also need Git and Make to work with RVComp. When running simulations through the Makefiles, remember to set the tool paths in the Makefile. After finishing the installations, continue with [the next page](./makesetup.md).

(setup-git-and-make-on-windows)=
## Setup Git and Make on Windows

Please install the Microsoft app installer from the Microsoft Store. Then open PowerShell with administrator privileges (Win+X, then `A`) and run:

```powershell
winget install --id Git.Git -e --source winget
winget install ezwinports.make
```

(rvcomp-install)=
## RVComp install

The RVComp source code is published on GitHub. Please clone it with:

```bash
$ git clone https://github.com/archlab-sciencetokyo/rvcomp.git
```

If you plan to simulate programs from external repositories (CoreMark, riscv-tests, embench-iot), either clone with the appropriate options or initialize the submodules after cloning:

```bash
$ cd rvcomp
$ git submodule update --init --recursive
```

(riscv-gnu-toolchain)=
## riscv-gnu-toolchain

Please install [riscv-gnu-toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain), which cross-compiles for the RISC-V ISA. You can build the bare-metal toolchain with `make`, and optionally build the Linux-targeting toolchain with `make linux`. Install the Linux version only if you need to build Linux; the bare-metal toolchain is sufficient for standard RVComp usage.

RVComp uses version 14.2.0. Other versions have not been validated. Installation on Windows is effectively unsupported, so build it on Linux or WSL2.

```bash
$ git clone https://github.com/riscv/riscv-gnu-toolchain
$ cd riscv-gnu-toolchain
$ git checkout 2025.01.20
```

Please install the required packages. For Ubuntu:

```bash
$ sudo apt-get install autoconf automake autotools-dev curl python3 python3-pip python3-tomli libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev ninja-build git cmake libglib2.0-dev libslirp-dev
```

Please generate the configuration (replace `<install dir>` as needed):

```bash
$ ./configure --prefix=<install dir> --with-arch=rv32ima_zicntr_zicsr_zifencei --with-abi=ilp32
```

Please build the bare-metal toolchain:

```bash
$ make -j$(nproc)
```

Please build the Linux-targeting toolchain:

```bash
$ make linux -j$(nproc)
```

If the installation fails, please try `make clean` and rerun the build commands, or rebuild in a minimal environment. After installation, please add the `bin` directory under the installation prefix to your `PATH`.

(vivado)=
## Vivado

As of October 2025, RVComp supports the AMD-based FPGA boards Nexys 4 DDR 100T and Arty A7 35T. Please install [Vivado Edition](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools/2024-1.html) for your OS to generate and load the FPGA bitstreams. We have validated version 2024.1.0 only.

If you use the bitstreams we provide and do not run place-and-route yourself, Vivado Lab Solutions is sufficient.

Vivado is supported only on x86_64 Linux or Windows. Use a virtual machine if you are on an Arm system.

(uv)=
## uv

[uv](https://github.com/astral-sh/uv) is a Python package manager used to install the dependencies for our serial communication application. Please install it with:

```bash
# On Linux
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

(xilinx-board-files)=
## Xilinx Board Files

If you use Vivado through the GUI you do not need this step. Otherwise, please install the board definition files for Nexys 4 DDR and Arty A7 from the [Xilinx Board Store](https://github.com/Xilinx/XilinxBoardStore):

```bash
$ git clone https://github.com/Xilinx/XilinxBoardStore
```

(device-tree-compiler)=
## device-tree-compiler

This tool compiles Linux device trees. Please install it with:

```bash
$ sudo apt-get install device-tree-compiler
```

(verilator)=
## Verilator

RVComp uses [Verilator](https://verilator.org/guide/latest/) for simulation. We have validated version 5.033.

Please follow the instructions below (also refer to the official guide). Install the prerequisite packages first:

```bash
$ sudo apt-get install git help2man perl python3 make autoconf flex bison
$ sudo apt-get install g++        # Or clang
$ sudo apt-get install libgz-dev  # Non-Ubuntu (ignore errors on Ubuntu)
$ sudo apt-get install libfl2     # Ubuntu only (ignore errors elsewhere)
$ sudo apt-get install libfl-dev  # Ubuntu only (ignore errors elsewhere)
$ sudo apt-get install zlibc zlib1g zlib1g-dev  # Ubuntu only (ignore errors elsewhere)
```

Then please build and install Verilator (replace `<install dir>`):

```bash
$ git clone https://github.com/verilator/verilator
$ cd verilator
$ git checkout v5.033
$ autoconf
$ unset VERILATOR_ROOT      # for bash
$ unsetenv VERILATOR_ROOT   # for csh
$ ./configure --prefix <install dir>
$ make -j$(nproc)
$ sudo make install
```

## Spike (Optional)

Spike is a RISC-V ISA simulator. Comparing its results with RVComp simulation traces helps check instruction correctness. The outputs will not match perfectly because Spike cannot omit unsupported CSRs, and timer values differ. We use version 1.1.1-dev, so please match that version if possible.

```bash
$ sudo apt install -y device-tree-compiler
$ git clone https://github.com/riscv-software-src/riscv-isa-sim.git
$ cd riscv-isa-sim
$ ./configure --prefix=<install dir> --with-target=riscv32-unknown-elf-gnu
$ make -j$(nproc)
$ make install
```

## GTKWave (Optional)

RVComp simulations can emit waveform dumps. Please install [GTKWave](http://gtkwave.sourceforge.net/) to view them:

```bash
$ sudo apt-get install gtkwave
```

## OpenSBI (Optional)

We maintain a fork of OpenSBI configured for RVComp. OpenSBI runs in RISC-V supervisor mode, abstracts privileged instructions, and hides hardware differences from the OS—making it necessary to boot Linux. The platform name is `rvcpu`, so please clone the repository as shown below.

```bash
$ git clone https://github.com/archlab-sciencetokyo/opensbi.git
```

## Buildroot (Optional)

We use [Buildroot](https://buildroot.org/) to build Linux images. Buildroot bundles the Linux kernel, C library, shell, and basic userland tools into a single build. We use version 2025.02; other versions are untested. Please download it from the [official site](https://buildroot.org/download.html) and extract the archive.

## Linux Kernel (Optional)

Download recent Linux kernels from [kernel.org](https://www.kernel.org/) if you want to try newer versions. We have verified only 6.9.0, 6.12.19, 6.13.0, and 6.14.2.
