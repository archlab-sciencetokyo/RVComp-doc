# Installation Guide

This section explains how to install the required tools.

If you are on Windows, begin with [Setup Git and Make on Windows](#setup-git-and-make-on-windows) to install the `git` and `make` commands. Please run [RVComp install](#rvcomp-install) first, then install the remaining tools.

The following tools are required for logic synthesis and place-and-route:

- [device-tree-compiler](#device-tree-compiler)
- [riscv-gnu-toolchain](#riscv-gnu-toolchain)
- [Vivado](#vivado)

The simulation flow requires:

- [riscv-gnu-toolchain](#riscv-gnu-toolchain)
- [Verilator](#verilator)

To use the serial communication utility we provide for the FPGA boards, install:

- [uv](#uv)



A Docker-based environment is available that provides all of the above tools except Vivado in a pre-configured container. See [Docker](#docker) for instructions.



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
$ git clone https://github.com/archlab-sciencetokyo/RVComp.git
```



The [Xilinx Board Files](https://github.com/Xilinx/XilinxBoardStore) are included as a git submodule under `tools/XilinxBoardStore`. Programs from external repositories (CoreMark, riscv-tests, embench-iot) are also submodules.



Initialize all submodules after cloning:

```bash
$ cd RVComp
$ git submodule update --init --recursive
```

To generate a bitstream with Vivado, the [Xilinx Board Files](https://github.com/Xilinx/XilinxBoardStore) are required. If you have not initialized all submodules, you can fetch only this one with:

```bash
$ git submodule update --init tools/XilinxBoardStore
```

(docker)=
## Docker



A Docker-based build environment is provided for Linux users. It bundles riscv-gnu-toolchain, Verilator, device-tree-compiler, and other required tools in a pre-configured image. **Vivado must still be installed natively on the host**; it cannot run inside the container.

### Installing Docker

**Linux:**

We recommend installing Docker in rootless mode so that the daemon runs as your user account without requiring `sudo`. Please follow the [official rootless installation guide](https://docs.docker.com/engine/security/rootless/) for your distribution. On Ubuntu, first install the prerequisites and configure subordinate UID/GID ranges:

```bash
$ sudo apt install -y dbus-user-session uidmap
$ sudo echo "$USER:231072:65536" >> /etc/subuid
$ sudo echo "$USER:231072:65536" >> /etc/subgid
```

Then run the rootless install script:

```bash
$ curl -fsSL https://get.docker.com/rootless | sh
```

Add the following lines to your `~/.bashrc` (or equivalent), replacing `<UID>` with the output of `id -u`:

```bash
export PATH=$HOME/bin:$PATH
export DOCKER_HOST=unix:///run/user/<UID>/docker.sock
```

Enable the Docker service for your user and allow it to run after logout:

```bash
$ systemctl --user enable --now docker
```

**Windows (WSL):**

Please install [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) and enable the WSL 2 backend in **Settings → Resources → WSL Integration**. Docker commands are then available directly inside your WSL distribution without any additional setup.

### Building the RVComp Docker image

From the `RVComp/` repository root, build the image with either of the following commands:

```bash
$ docker build -t rvcomp:latest .
```

```bash
$ ./tools/setup.sh
```

### Enabling and disabling Docker in the build

The `GNUmakefile` in the RVComp repository root contains a `DOCKER` variable that controls whether commands are delegated to the container:

- Set `DOCKER=1` (the default) to delegate Docker-compatible targets to the container.
- Set `DOCKER=0` to run commands directly on the host.

You can either edit `GNUmakefile` directly or override it on the command line:

```bash
$ make DOCKER=1 isa
$ make DOCKER=1 menuconfig
$ make DOCKER=0 bit
```

When `DOCKER=1`, `make` starts the container automatically before executing Docker-compatible targets. The following targets remain on the host even when Docker is enabled, because they require Vivado or direct access to local devices: `bit`, `rebit`, `reclockbit`, `load`, `remoteload`, `termnb`, `term`, and `config`.

`menuconfig` and `cliconfig` are delegated to the container with an interactive TTY when Docker is enabled. This lets you use the configuration UI without installing the Python dependencies on the host.

### Using the container interactively

To open a shell inside the container with the repository mounted, run the following from the `RVComp/` root:

```bash
$ docker run -it --rm -v $(pwd):/workspace rvcomp:latest bash
```



(vivado)=
## Vivado

As of October 2025, RVComp supports the AMD-based FPGA boards Nexys 4 DDR 100T and Arty A7 35T. Please install [Vivado Edition](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools/2024-1.html) for your OS to generate and load the FPGA bitstreams. We have validated version 2024.1.0 only.

If you use the bitstreams we provide and do not run place-and-route yourself, Vivado Lab Solutions is sufficient.

Vivado is supported only on x86_64 Linux or Windows. Use a virtual machine if you are on an Arm system.



Vivado is **not** available inside the Docker container. It must be installed natively on the host regardless of whether Docker is used for other tools.



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

We use [Buildroot](https://buildroot.org/) to build Linux images. Buildroot bundles the Linux kernel, C library, shell, and basic userland tools into a single build. Please download it from the [official site](https://buildroot.org/download.html) and extract the archive.



The recommended way to build Linux for RVComp is through the [RVComp-buildenv](https://github.com/archlab-sciencetokyo/RVComp-buildenv) repository, which provides a pre-configured Buildroot external tree. See [Linux Build](build.md) for details.


