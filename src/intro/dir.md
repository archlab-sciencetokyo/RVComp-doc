# Directory Explanation

This section explains the directory structure of the RVComp project. The project is organized by functionality, with each directory having a specific role.

## Project Root Structure

```
RVComp/
├── bootrom/              # Bootrom-related files
├── buildroot/            # Buildroot external tree configuration files
├── constr/               # FPGA constraint files
├── fpga/                 # FPGA-related files (tcl scripts)
├── image/                # Linux payloads
├── prog/                 # Programs for simulation
├── src/                  # RTL source code
├── test/                 # Testbenches
├── tools/                # Utilities, configuration tool, and board-file submodule
├── vivado/               # Vivado project directory
├── config.mk             # User configuration file
├── Dockerfile            # Docker image definition
├── GNUmakefile           # Docker delegation layer for make
└── Makefile              # Main build file
```

## Main Directory Details

### bootrom/ - Bootrom

ROM image executed at boot and files necessary for its generation.

```
bootrom/
├── src/                  # Bootloader source code
│   ├── bootloader.c          # Main bootloader (UART/MMC boot logic)
│   ├── bootrom.S             # Assembly entry point
│   ├── io.h                  # I/O helper macros
│   ├── linker.ld             # Linker script for bootrom
│   ├── rvcomp_ether.c        # Ethernet driver
│   ├── rvcomp_ether.h        # Ethernet driver header
│   ├── rvcomp_mmc.c          # MMC driver
│   ├── rvcomp_mmc.h          # MMC driver header
│   ├── rvcomp_uart.c         # UART driver
│   └── rvcomp_uart.h         # UART driver header
├── bootrom.v             # Bootrom RTL
├── Makefile              # Bootrom build file
└── rvcomp.dts            # Device tree source
```

Bootrom roles:
- System initialization
- Device tree provision
- UART boot functionality
- MMC boot functionality (Nexys 4 DDR only)
- Jump to OpenSBI or application

### buildroot/ - Buildroot External Tree

Buildroot external tree for building Linux images. Contains defconfigs, kernel configs, custom packages, and overlay files.

```
buildroot/
├── configs/              # Buildroot defconfig files for each boot mode
│   ├── mmc_defconfig                    # Buildroot config for MMC boot (Linux image + OpenSBI)
│   ├── mmc_rootfs_second_pass.fragment  # Config fragment for second-pass rootfs build
│   └── uart_defconfig                   # Buildroot config for UART boot
├── kernel/               # Linux kernel defconfig files
│   ├── mmc/                    # Kernel config for MMC boot
│   │   └── defconfig               # Kernel defconfig for MMC boot
│   └── uart/                   # Kernel config for UART boot
│       └── defconfig               # Kernel defconfig for UART boot
├── package/              # Custom Buildroot packages
│   ├── rvcomp-bootfiles/       # Package providing init scripts for boot
│   │   ├── files/                  # Init script files
│   │   │   ├── S20-rvcomp-ethernet     # Ethernet interface init script
│   │   │   ├── S30-rvcomp-mmc-rootfs   # MMC root filesystem mount script
│   │   │   └── init                    # Early init script
│   │   ├── Config.in               # Package configuration menu
│   │   └── rvcomp-bootfiles.mk     # Buildroot package definition
│   ├── rvcomp-ethernet/        # Ethernet kernel driver package
│   │   ├── src/                    # Driver source
│   │   │   ├── Makefile                # Driver build script
│   │   │   └── rvcomp_ethernet.c       # Ethernet driver
│   │   ├── Config.in               # Package configuration menu
│   │   └── rvcomp-ethernet.mk      # Buildroot package definition
│   └── rvcomp-mmc/             # MMC kernel driver package
│       ├── src/                    # Driver source
│       │   ├── Makefile                # Driver build script
│       │   └── rvcomp_mmc.c            # MMC driver
│       ├── Config.in               # Package configuration menu
│       └── rvcomp-mmc.mk           # Buildroot package definition
├── rootfs_overlay/       # Files overlaid onto the root filesystem
│   └── usr/
│       └── bin/
│           └── rv_atomic_write         # Atomic write utility for RVComp
├── scripts/              # Post-build scripts
│   └── post_image_script.sh    # Combines fw_payload.bin and rootfs.ext4 into a single image
├── Config.in             # Top-level package menu
├── external.desc         # Buildroot external tree description
└── external.mk           # Buildroot external tree makefile
```

### constr/ - FPGA Constraint Files

Contains constraint files defining pin assignments, etc.

```
constr/
├── Arty-A7-35T-Master.xdc       # Arty A7-35 constraints
├── Arty-Mig.ucf                 # Arty A7 MIG constraints
├── Nexys-A7-100T-Master.xdc     # Nexys A7 100T constraints
└── Nexys-Mig.ucf                # Nexys A7 100T MIG constraints
```

### fpga/ - FPGA-related Files

Contains files necessary for FPGA synthesis and bitstream generation.

```
fpga/
└── Xilinx/
    ├── arty_a7/              # Arty A7 specific files
    │   └── mig.prj               # MIG configuration file (DDR3)
    ├── nexys4ddr/            # Nexys 4 DDR specific files
    │   └── mig.prj               # MIG configuration file (DDR2)
    ├── build.tcl             # Project creation script
    ├── load.tcl              # Local load script
    ├── load_remote.tcl       # Remote load script
    ├── rebuild.tcl           # Rebuild script
    └── reclock.tcl           # Clock frequency change script
```



Note: the Xilinx Board Store checkout lives under `tools/XilinxBoardStore`, not under `fpga/`. It is populated automatically by `git submodule update --init --recursive`.



### image/ - Linux Payloads

Contains the Linux payload and files for simulation.

```
image/
├── fw_payload.128.hex    # 128-bit wide hex of fw_payload.bin; used for simulation
├── fw_payload.bin        # Linux payload (OpenSBI + kernel + initramfs)
└── Makefile              # Converts fw_payload.bin to fw_payload.128.hex for simulation
```

### prog/ - Test Programs and Benchmarks

Test suites and simulation programs are in respective directories.

```
prog/
├── coremark/             # CoreMark benchmark wrapper
│   ├── coremark/             # CoreMark git submodule
│   ├── riscv/                # RISC-V port files
│   │   ├── core_portme.c         # Platform-specific CoreMark port
│   │   ├── core_portme.h         # Platform-specific CoreMark port header
│   │   ├── crt0.S                # C runtime startup (assembly)
│   │   ├── cvt.c                 # Integer-to-string conversion
│   │   ├── ee_printf.c           # Minimal printf implementation
│   │   └── link.ld               # Linker script
│   ├── LICENSE.md            # CoreMark license
│   └── Makefile              # Build script for CoreMark
├── embench-iot/          # Embench-IoT benchmark wrapper
│   ├── embench-iot/          # Embench-IoT git submodule
│   ├── riscv/                # RISC-V port files
│   │   └── arch.cfg              # Architecture configuration for Embench-IoT
│   ├── COPYING               # Embench-IoT license
│   └── Makefile              # Build script for Embench-IoT
├── riscv-tests/          # RISC-V test suite wrapper
│   ├── riscv-tests/          # riscv-tests git submodule
│   ├── env/                  # Test environment files
│   │   ├── encoding.h            # RISC-V encoding definitions
│   │   └── link.ld               # Linker script for tests
│   ├── LICENSE               # riscv-tests license
│   └── Makefile              # Build script for riscv-tests
└── rvtest/               # Custom test programs
    ├── crt0.S                # C runtime startup (assembly)
    ├── io.h                  # I/O helper macros
    ├── link.ld               # Linker script
    ├── main.c                # Hello World example
    └── Makefile              # Build script for custom tests
```

### src/ - RTL Source Code

Directory containing RTL (Register Transfer Level) design files.

```
src/
├── cache/                # Cache
│   ├── l1_dcache.v           # L1 data cache
│   ├── l1_icache.v           # L1 instruction cache
│   └── l2_cache.v            # L2 unified cache
├── clint/                # Core-Local Interrupt Controller
│   └── clint.v               # CLINT module
├── cpu/                  # CPU core (5-stage pipeline: IFU → Decoder → ALU → LSU → WB)
│   ├── alu.v                 # Arithmetic Logic Unit
│   ├── amo_decoder.v         # Atomic instruction decoder (A extension)
│   ├── amoalu.v              # Atomic operation ALU (A extension)
│   ├── bimodal.v             # Bimodal branch predictor
│   ├── bru.v                 # Branch resolution unit
│   ├── cpu.v                 # CPU top module
│   ├── csr_regfile.v         # CSR file
│   ├── csralu.v              # Arithmetic unit for Zicsr instructions
│   ├── decoder.v             # Instruction decoder
│   ├── divider.v             # Divider (M extension)
│   ├── ifu.v                 # Instruction fetch unit + L0 instruction cache
│   ├── imm_gen.v             # Immediate generator
│   ├── lsu.v                 # Load/Store unit
│   ├── multiplier.v          # Multiplier (M extension)
│   └── regfile.v             # Register file
├── dram/                 # DRAM controller (DDR2/DDR3)
│   └── dram_controller.v     # DRAM controller (MIG DDR2/DDR3 interface)
├── ether/                # Ethernet MAC controller (10/100 Mbps)
│   ├── ether_mii.v           # Ethernet wrapper for Arty A7 (MII)
│   ├── ether_rmii.v          # Ethernet wrapper for Nexys 4 DDR (RMII)
│   ├── ether_rx_mii.v        # MII receive path
│   ├── ether_rx_rmii.v       # RMII receive path
│   ├── ether_tx_mii.v        # MII transmit path
│   ├── ether_tx_rmii.v       # RMII transmit path
│   └── sdp_2_clock_ram.v     # Dual-clock RX/TX buffer RAM
├── mmu/                  # Memory management unit (SV32)
│   ├── dtlb.v                # Data TLB
│   ├── itlb.v                # Instruction TLB
│   ├── mmu.v                 # MMU top module (ITLB/DTLB/PTW/L1I$/L1D$ integration)
│   └── ptw.v                 # Page table walker
├── plic/                 # Platform-Level Interrupt Controller
│   └── plic.v                # PLIC module (external interrupt management, priority control)
├── sdcram/               # RAM-like storage access wrapper with cache
│   ├── cache_tags.v              # Cache tag memory
│   ├── cmd_rom.v                 # Initialization command ROM
│   ├── sdcram_cmd_transceiver.v  # Command line transceiver
│   ├── sdcram_protocol.v         # Command/data state machine
│   ├── sdcram_crc_16.v            # CRC-16 computation
│   ├── sdcram_crc_7.v             # CRC-7 computation
│   ├── sdcram_dat_transceiver.v  # Data line transceiver
│   ├── sdcram_interface.v        # Interface
│   ├── sdcram.v                  # Cache and storage access core
│   ├── sdcram_controller.v       # AXI/MMIO wrapper for sdcram
│   └── tdp_rf_bw2clk.v          # True dual-port RAM with byte-write and two clocks
├── soc/                  # System-on-Chip (RTL top module)
│   ├── axi_interconnect.v    # AXI4 Lite Based interconnect
│   └── soc.v                 # SoC top module (CPU, cache, MMU, peripheral integration)
├── sram/                 # SRAM controller
│   └── sram.v                # SRAM (currently uses DRAM, can be replaced with SRAM if DRAM not needed)
├── uart/                 # UART controller
│   ├── fifo.v                # FIFO for transmit/receive buffer
│   ├── uart.v                # UART top module
│   ├── uart_rx.v             # UART receiver
│   └── uart_tx.v             # UART transmitter
├── axi.vh                # Bus-related definitions
├── config.vh             # Modifiable hardware configuration header file
├── rvcom.vh              # Constant definition header file (encoding, etc.)
├── async_fifo.v          # Asynchronous FIFO (inter-clock domain data transfer)
└── synchronizer.v        # Clock domain crossing synchronization circuit
```

### test/ - Testbenches

Contains testbench files for simulation.

```
test/
├── BUFG.sv               # Xilinx primitive mock
├── clk_wiz_0.sv          # Clock generation mock
├── clk_wiz_1.sv          # Clock generation mock
├── IBUF.sv               # Xilinx primitive mock
├── mig_7series_0.sv      # MIG memory controller mock
└── top.sv                # Top-level testbench
```

### tools/

Utility scripts, the serial communication program, and the Xilinx Board Store submodule.

```
tools/
├── XilinxBoardStore/     # Xilinx Board Store git submodule
├── pyproject.toml        # Python project config (uv dependencies)
├── README.md             # Tools directory README
├── setting.py            # menuconfig-style configuration utility (make menuconfig / make cliconfig)
├── setup.sh              # Docker image build helper
├── term.py               # Serial communication program (make term / make termnb)
└── uv.lock               # uv dependency lock file
```

### vivado/ - Vivado Project

By default, `make bit` command generates project under this directory.

### config.mk

User-specific configuration file. Used to specify absolute paths, etc.

### Dockerfile

Docker image definition for the build environment.



### GNUmakefile

Docker delegation layer that GNU make reads before `Makefile`. The `DOCKER` variable controls whether Docker-compatible targets are delegated to the container (`DOCKER=1`, the default) or run directly on the host (`DOCKER=0`). See the [Installation Guide](install.md) for Docker setup details.



### Makefile

Main build rules for simulation, bootrom generation, FPGA synthesis, and utility targets. Refer to [Make Command](make.md).

## Build Artifacts

### obj_dir/
C++ code generated by Verilator and compiled simulator.

### log/
Log files generated during simulation execution.
Generated when options are specified.
For options, refer to [Make Command](make.md).

```
log/
├── commit.log            # Commit log
├── diff/                 # Spike comparison results
├── dump.fst              # Waveform file
├── dump.vcd              # Waveform file
├── trace_dmem.log        # Data memory trace
└── trace_rf.log          # Register file trace
```
