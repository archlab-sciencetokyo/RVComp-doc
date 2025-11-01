# Make Command

This section explains the main `make` targets and options in the RVComp project. The `Makefile` in the repository root automates simulation, verification, FPGA synthesis, and other tasks.

## FPGA targets

### bootrom

```bash
$ make bootrom
```

Builds the program and device tree stored in the boot ROM. If you launch Vivado in the GUI, you must build the boot ROM image manually.

### bit

```bash
$ make bit
```

Generates the FPGA bitstream. The recipe performs the following steps:

1. Clean and rebuild the boot ROM
2. Run Vivado for logic synthesis, place-and-route, and bitstream generation

### rebit

```bash
$ make rebit
```

Regenerates the bitstream using the existing Vivado project. Skipping project recreation makes it faster than `make bit`.

### load

```bash
$ make load
```

Loads the generated bitstream onto a locally connected FPGA board.

### remoteload

```bash
$ make remoteload
```

Loads the bitstream onto a remote FPGA over the network. The remote host must be running a compatible version of the Vivado Hardware Server.

### term

```bash
$ make term
```

Launches the serial communication program and opens a connection to the FPGA. When the program receives `!\n`, it sends the Linux image specified by the `linux_image` variable in the Makefile (default `./image/fw_payload.bin`) to the FPGA and boots Linux. The bootloader (`bootrom/src/bootloader.c`) first transmits `Hello World!\n`; the final two characters are used to detect that the FPGA has finished booting. To exit the serial console, please press `Ctrl+C` followed by `:q`.

### config

```bash
$ make config
```

Loads the bitstream onto the FPGA and transfers the Linux image (local FPGA only).

## Simulation options

Please pass the following variables to adjust simulation and debugging behavior:

- `DISPLAY_CYCLES=<cycles>`: Interval for printing cycle counts
- `MAX_CYCLES=<cycles>`: Maximum number of simulation cycles
- `DEBUG_ENABLE_LOG=1`: Enable debug logging
- `MEM_FILE=<file>`: Memory initialization file
- `COMMIT_LOG_FILE=<file>`: Generate a commit log at the specified path
- `TRACE_VCD_FILE=<file>`: Generate a VCD waveform file
- `TRACE_FST_FILE=<file>`: Generate an FST waveform file
- `TRACE_RF_FILE=<file>`: Dump register-file traces
- `TRACE_DMEM_FILE=<file>`: Dump data-memory traces
- `NO_UART_BOOT=1`: Disable UART boot and start with DRAM preloaded
- `DIFF_SPIKE=1`: Compare instruction results with Spike and save the diff to `log/diff`

## RISC-V ISA tests

Runs [riscv-tests](https://github.com/riscv-software-src/riscv-tests), located under `prog/riscv-tests`.

### isa

```bash
$ make isa
```

Runs every RISC-V ISA test. Depending on configuration, this includes:

- RV32UI (user-level integer)
- RV32UM (user-level multiply/divide) when `RVM=1`
- RV32UA (user-level atomic) when `RVA=1`
- RV32SI (supervisor) when `RVS=1`
- RV32MI (machine) when `RVS=0`

### Target environment

You can set `TGT_ENV` to select the execution mode:

- `p`: physical address mode
- `v`: virtual address mode (Sv32)

### Individual suites

```bash
$ make rv32ui_test  # Integer instruction tests
$ make rv32um_test  # Multiply/divide instruction tests
$ make rv32ua_test  # Atomic instruction tests
$ make rv32si_test  # Supervisor-mode tests
$ make rv32mi_test  # Machine-mode tests
```

### Individual test cases

```bash
$ make add   # Runs rv32ui-p-add
$ make mul   # Runs rv32um-p-mul
$ make lrsc  # Runs rv32ua-p-lrsc
```

Available tests:

- **rv32ui**: add, addi, sub, and, andi, or, ori, xor, xori, sll, slli, srl, srli, sra, srai, slt, slti, sltiu, sltu, beq, bge, bgeu, blt, bltu, bne, jal, jalr, sb, sh, sw, lb, lbu, lh, lhu, lw, auipc, lui, fence_i, ma_data, simple
- **rv32um**: mul, mulh, mulhsu, mulhu, div, divu, rem, remu
- **rv32ua**: amoadd_w, amoand_w, amomax_w, amomaxu_w, amomin_w, amominu_w, amoor_w, amoxor_w, amoswap_w, lrsc
- **rv32si**: csr, dirty, ma_fetch, scall, sbreak, wfi
- **rv32mi**: breakpoint, csr, mcsr, illegal, ma_fetch, ma_addr, scall, sbreak, shamt, lw-misaligned, lh-misaligned, sh-misaligned, sw-misaligned, zicntr

## CoreMark

```bash
$ make coremark
```

Runs the [CoreMark](https://github.com/eembc/coremark) benchmark located under `prog/coremark`.

## Embench-IoT

```bash
$ make embench
```

Runs every [Embench-IoT](https://github.com/embench/embench-iot) benchmark located under `prog/embench-iot`.

To run a specific benchmark:

```bash
$ make aha-mont64
$ make crc32
$ make cubic
$ make edn
$ make huffbench
# ...
```

Available benchmarks: aha-mont64, crc32, cubic, edn, huffbench, matmult-int, md5sum, minver, nbody, nettle-aes, nettle-sha256, nsichneu, picojpeg, primecount, qrduino, sglib-combined, slre, st, statemate, tarfind, ud, wikisort

## Custom tests

```bash
$ make rvtest
```

Runs the programs under `rvtest/`. Currently this directory contains only the Hello World example.

## linux

```bash
$ make linux
```

Simulates the Linux boot process.

## Clean commands

### clean

```bash
$ make clean
```

Removes simulation artifacts:

- `obj_dir/` (Verilator output)
- `log/` (simulation logs)
- `*.vcd`, `*.fst` (waveform files)
- Generated files under `bootrom/`

### progclean

```bash
$ make progclean
```

Removes program build artifacts:

- `riscv-tests`
- `coremark`
- `embench-iot`
- `rvtest`

### vivadoclean

```bash
$ make vivadoclean
```

Removes Vivado-generated artifacts:

- `.Xil/`
- `vivado*.jou`, `vivado*.log`
- `.cache`, `.hw`, `.runs`, `.sim`, and similar directories inside `vivado/`

### distclean

```bash
$ make distclean
```

Performs `clean`, `progclean`, and `vivadoclean` in one step.
