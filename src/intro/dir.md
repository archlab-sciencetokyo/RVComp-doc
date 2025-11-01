# Directory Explanation

This section explains the directory structure of the RVComp project. The project is organized by functionality, with each directory having a specific role.

## Project Root Structure

```
rvcom/
├── bootrom/              # Bootrom-related files
├── buildroot/            # Buildroot configuration files
├── constr/               # FPGA constraint files
├── fpga/                 # FPGA-related files (tcl scripts)
├── prog/                 # Programs for simulation
├── src/                  # RTL source code
├── test/                 # Testbenches
├── vivado/               # Vivado project directory
├── config.mk             # User configuration file
├── Makefile              # Main build file
└── setting.py            # Configuration change script
```

## Main Directory Details

### src/ - RTL Source Code

Directory containing RTL (Register Transfer Level) design files.

```
src/
├── cache/                # Cache
│   ├── l1_dcache.v         # L1 data cache
│   ├── l1_icache.v         # L1 instruction cache
│   └── l2_cache.v          # L2 unified cache
├── clint/                # Core-Local Interrupt Controller
│   └── clint.v             # CLINT module
├── cpu/                  # CPU core (5-stage pipeline: IFU → Decoder → ALU → LSU → WB)
│   ├── alu.v               # Arithmetic Logic Unit
│   ├── amo_decoder.v       # Atomic instruction decoder (A extension)
│   ├── amoalu.v            # Atomic operation ALU (A extension)
│   ├── bimodal.v           # Bimodal branch predictor
│   ├── bru.v               # Branch resolution unit
│   ├── cpu.v               # CPU top module
│   ├── csralu.v            # Arithmetic unit for Zicsr instructions
│   ├── csr_regfile.v       # CSR file
│   ├── decoder.v           # Instruction decoder
│   ├── divider.v           # Divider (M extension)
│   ├── ifu.v               # Instruction fetch unit + L0 instruction cache
│   ├── imm_gen.v           # Immediate generator
│   ├── lsu.v               # Load/Store unit
│   ├── multiplier.v        # Multiplier (M extension)
│   └── regfile.v           # Register file
├── dram/                 # DRAM controller (DDR2/DDR3)
│   ├── async_fifo.v        # Asynchronous FIFO (inter-clock domain data transfer)
│   └── dram_controller.v   # DRAM controller (MIG DDR2/DDR3 interface)
├── mmu/                  # Memory management unit (SV32)
│   ├── dtlb.v              # Data TLB
│   ├── itlb.v              # Instruction TLB
│   ├── mmu.v               # MMU top module (ITLB/DTLB/PTW/L1I$/L1D$ integration)
│   └── ptw.v               # Page table walker
├── plic/                 # Platform-Level Interrupt Controller
│   └── plic.v              # PLIC module (external interrupt management, priority control)
├── soc/                  # System-on-Chip (RTL top module)
│   ├── axi_interconnect.v  # AXI4 Lite Based interconnect
│   └── soc.v               # SoC top module (CPU, cache, MMU, peripheral integration)
├── sram/                 # SRAM controller
│   └── sram.v              # SRAM (currently uses DRAM, can be replaced with SRAM if DRAM not needed)
├── uart/                 # UART controller
│   ├── fifo.v              # FIFO for transmit/receive buffer
│   ├── uart.v              # UART top module
│   ├── uart_rx.v           # UART receiver
│   └── uart_tx.v           # UART transmitter
├── axi.vh                # Bus-related definitions
├── config.vh             # Modifiable hardware configuration header file
├── rvcom.vh              # Constant definition header file (encoding, etc.)
└── synchronizer.v        # Clock domain crossing synchronization circuit
```

### bootrom/ - Bootrom

ROM image executed at boot and files necessary for its generation.

```
bootrom/
├── Makefile              # Bootrom build file
├── bootrom.v             # Bootrom RTL
├── rvcom.dts             # Device tree source
└── src/                  # Primary bootloader source code
```

Bootrom roles:
- System initialization
- Device tree provision
- UART boot functionality (optional)
- Jump to OpenSBI or application

### test/ - Testbenches

Contains testbench files for simulation.

```
test/
├── top.sv                # Top-level testbench
├── BUFG.sv               # Xilinx primitive mock
├── clk_wiz_0.sv          # Clock generation mock
├── clk_wiz_1.sv          # Clock generation mock
├── IBUF.sv               # Xilinx primitive mock
└── mig_7series_0.sv      # MIG memory controller mock
```


### prog/ - Test Programs and Benchmarks

Test suites and simulation programs are in respective directories.

```
prog/
├── riscv-tests/          # RISC-V test suite
├── coremark/             # CoreMark benchmark
├── embench-iot/          # Embench-IoT benchmark
└── rvtest/               # Custom test programs
```

### fpga/ - FPGA-related Files

Contains files necessary for FPGA synthesis and bitstream generation.

```
fpga/
└── Xilinx/
    ├── build.tcl         # Project creation script
    ├── rebuild.tcl       # Rebuild script
    ├── reclock.tcl       # Clock frequency change script
    ├── load.tcl          # Local load script
    ├── load_remote.tcl   # Remote load script
    ├── nexys4ddr/        # Nexys 4 DDR specific files
    │   └── mig.prj       # MIG configuration file (DDR2)
    └── arty_a7/          # Arty A7 specific files
        └── mig.prj       # MIG configuration file (DDR3)
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

### vivado/ - Vivado Project

By default, `make bit` command generates project under this directory.

<!-- ### pytest/ - Pytest Test Suite

Automated tests using Python testing framework.

```
pytest/
├── test_*.py             # Test scripts
├── nlogs/                # Test logs
└── tlogs/                # Timing logs
``` -->

<!-- ### image/ - Linux Images

Binary images of Linux kernel and filesystem.

```
image/
├── linux-6.9.bin         # Linux kernel image
└── ...
```

These images are transferred to FPGA with `make config` command. -->

<!-- ### buildroot/ - Buildroot Configuration

Buildroot configuration files for building embedded Linux systems. -->


### Makefile
Main build file. Contains target definitions, source specifications, and build rules.
Refer to [Make Command](make.md).

### config.mk
User-specific configuration file.
Used to specify absolute paths, etc.


### setting.py
Python script for changing hardware configuration.
Refer to the [Config chapter](config.md).


## Build Artifacts

### obj_dir/
C++ code generated by Verilator and compiled simulator.

### log/
Log files generated during simulation execution.
Generated when options are specified.
For options, refer to [Make Command](make.md).

```
log/
├── dump.fst              # Waveform file
├── dump.vcd              # Waveform file
├── commit.log            # Commit log
├── trace_rf.log          # Register file trace
├── trace_dmem.log        # Data memory trace
└── diff/                 # Spike comparison results
```
