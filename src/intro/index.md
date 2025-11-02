# Introduction

## About RVComp

RVComp is a RISC-V SoC (System on Chip) with a five-stage pipeline. It supports the RV32IMASU_Zicntr_Zicsr_Zifencei instruction set, including privileged modes and the Sv32 virtual memory system, so it can run Linux. The RVComp project began in June 2024 and offers the following characteristics:

- **High operating frequency**: Achieves a maximum clock frequency of **170 MHz** on a Nexys A7-100T (XC7A100T-1CSG324C)
- **HDL implementation**: About 7,757 lines of Verilog HDL (as of October 2025), with a from-scratch design except for the DRAM controller and clock generation
- **Permissive licensing**: All HDL components except IP are provided under the MIT license

## LICENSE

RVComp files we developed from scratch are distributed under the [MIT license](https://opensource.org/licenses/MIT), so the project source code can be freely used, modified, and redistributed. 

However, please note that the RVComp project uses multiple open-source components.
The following components follow their respective licenses; see the LICENSE file for full details.

- **DRAM controller**: [Xilinx MIG](https://www.amd.com/en/products/adaptive-socs-and-fpgas/intellectual-property/mig.html#documentation) ([Xilinx End User License Agreement](https://account.amd.com/content/dam/account/en/licenses/download/end-user-license-agreement.pdf))
- **Clock generation**: Xilinx Clocking Wizard ([Xilinx End User License Agreement](https://account.amd.com/content/dam/account/en/licenses/download/end-user-license-agreement.pdf))
- **prog/coremark**: [CoreMark](https://github.com/eembc/coremark) ([COREMARK® ACCEPTABLE USE AGREEMENT + Apache License 2.0](https://github.com/eembc/coremark?tab=License-1-ov-file))
- **prog/embench**: [Embench-IoT](https://github.com/embench/embench-iot) ([GPL-3.0 License](https://github.com/embench/embench-iot?tab=GPL-3.0-1-ov-file))
- **prog/riscv-tests**: [riscv-tests](https://github.com/riscv/riscv-tests) ([The Regents of the University of California (Regents)](https://github.com/riscv-software-src/riscv-tests?tab=License-1-ov-file))

- **OpenSBI**: [OpenSBI for customized for RVComp](https://github.com/archlab-sciencetokyo/opensbi.git) ([BSD-2-Clause License](https://github.com/archlab-sciencetokyo/opensbi?tab=License-1-ov-file))

### System overview

For the overall system structure, refer to [SoC Architecture](../arch/index.md).

## Supported instruction sets

- **Base ISA**: RV32I (integer)
- **Extensions**:
  - M extension: multiplication and division instructions
  - A extension: atomic instructions (LR/SC and AMO)
  - S extension: supervisor mode
  - U extension: user mode
  - Zicntr: counter access instructions
  - Zicsr: CSR access instructions
  - Zifencei: instruction-fetch fences
- **Virtual memory**: Sv32 (two-level page tables with 4 KB pages)

## Development environment

- **OS**: Ubuntu 22.04 LTS (x86_64)
- **Cross-compiler**: riscv-gnu-toolchain (14.2.0)
- **HDL**: Verilog HDL for RTL, SystemVerilog for the testbench
- **Simulator**: Verilator (v5.033)
- **FPGA synthesis**: Vivado Edition 2024.1
- **Supported boards**:
  - Nexys 4 DDR 100T (DDR2, 128 MB)
  - Arty A7 35T (DDR3, 256 MB)

We develop on Ubuntu 22.04 LTS, and this guide is primarily written for that environment. We have also confirmed operation on Windows 11 Education, but some tools do not provide Windows installers, so WSL2 is required in those cases. Commands in the Makefiles use Unix conventions, so WSL2 is recommended for Windows users. Some tools do not support Arm environments. If you plan to work on Arm hardware, consider using an x86_64 virtual machine.

## Verification status

RVComp has been validated in simulation using the following test suites:

- **riscv-tests**: Covers the RISC-V ISA(RV32IMASU) (passes all tests except `ma_data`)
- **riscv-arch-test**: Passes every test(RV32IMASU) when compared against Spike via RISCOF

The `ma_data` test in riscv-tests checks misaligned accesses. Implementing hardware support for this rarely used feature would add significant complexity, so handling it with software exceptions is acceptable. RVComp intentionally raises a software exception instead, which is why the test does not pass. We also boot Linux kernel 6.13.0, run the CoreMark-PRO benchmark in validation mode, and confirm that it produces the expected results.
