# Introduction

## About RVComp

RVComp is a RISC-V SoC (System-on-Chip) featuring a five-stage pipeline. It supports the RV32IMA_Zicntr_Zicsr_Zifencei instruction set, along with M-, S-, and U-modes, the privileged architecture, and the Sv32 virtual memory system, enabling it to run Linux. The RVComp project began in June 2024 and offers the following characteristics:

- **High operating frequency**: Achieves a maximum clock frequency of **160 MHz** (Version 1.1.2) on a Nexys A7-100T (XC7A100T-1CSG324C)
- **HDL implementation**: RVComp is described in Verilog HDL with a from-scratch design except for the DRAM controller and clock generation
- **Permissive licensing**: All HDL components except IP are provided under the MIT license
- **Ethernet support**: 100 Mbps Ethernet controller with RMII (Nexys 4 DDR) and MII (Arty A7) interfaces, including hardware MAC filtering and FCS computation
- **microSD boot support**: microSD controller enabling Linux to boot and operate from a microSD card on the Nexys 4 DDR board
- **Interactive configuration**: Various SoC parameters can be configured through a terminal-based GUI (`tools/setting.py`)
- **Docker support**: Containerized build environment with simulation tools pre-installed (Vivado must be installed natively)




- **Ethernet support**: 100 Mbps Ethernet controller with RMII (Nexys 4 DDR) and MII (Arty A7) interfaces, including hardware MAC filtering and FCS computation
- **microSD boot support**: microSD controller enabling Linux to boot and operate from a microSD card on the Nexys 4 DDR board
- **Interactive configuration**: Various SoC parameters can be configured through a terminal-based GUI (`tools/setting.py`)
- **Docker support**: Containerized build environment with simulation tools pre-installed (Vivado must be installed natively)



## LICENSE



RVComp files we developed from scratch are distributed under the [MIT license](https://opensource.org/licenses/MIT).



However, please note that the RVComp project uses multiple open-source components.
The following components follow their respective licenses; see the LICENSE file for full details.

- **DRAM controller**: [Xilinx MIG](https://www.amd.com/en/products/adaptive-socs-and-fpgas/intellectual-property/mig.html#documentation) ([Xilinx End User License Agreement](https://account.amd.com/content/dam/account/en/licenses/download/end-user-license-agreement.pdf))
- **Clock generation**: Xilinx Clocking Wizard ([Xilinx End User License Agreement](https://account.amd.com/content/dam/account/en/licenses/download/end-user-license-agreement.pdf))
- **prog/coremark**: [CoreMark](https://github.com/eembc/coremark) ([COREMARK® ACCEPTABLE USE AGREEMENT + Apache License 2.0](https://github.com/eembc/coremark?tab=License-1-ov-file))
- **prog/embench**: [Embench-IoT](https://github.com/embench/embench-iot) ([GPL-3.0 License](https://github.com/embench/embench-iot?tab=GPL-3.0-1-ov-file))
- **prog/riscv-tests**: [riscv-tests](https://github.com/riscv/riscv-tests) ([The Regents of the University of California (Regents)](https://github.com/riscv-software-src/riscv-tests?tab=License-1-ov-file))
- **OpenSBI**: [OpenSBI customized for RVComp](https://github.com/archlab-sciencetokyo/opensbi.git) ([BSD-2-Clause License](https://github.com/archlab-sciencetokyo/opensbi?tab=License-1-ov-file))


- **buildroot**: Device drivers, configuration files, and patches to build Linux ([GPL-2.0 License](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)).
- **RVComp-buildenv**: Build scripts that use Buildroot to produce Linux images ([GPL-2.0 License](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)). Prebuilt Linux images also include third-party software such as Linux and OpenSBI, so redistribution must follow the licenses of those components.
- **tools/XilinxBoardStore**: [Xilinx Board Store](https://github.com/Xilinx/XilinxBoardStore) ([Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0))



### System overview

For the overall system structure, refer to [SoC Architecture](../arch/index.md).

## Supported instruction sets

- **Base ISA**: RV32I (integer)
- **Extensions**:
  - M extension: multiplication and division instructions
  - A extension: atomic instructions (LR/SC and AMO)
  - Zicntr: counter access instructions
  - Zicsr: CSR access instructions
  - Zifencei: instruction-fetch fences
- **Virtual memory**: Sv32 (two-level page tables with 4 KB pages)

## Development environment

- **OS**: Ubuntu 22.04 LTS (x86_64)
- **Cross-compiler**: riscv-gnu-toolchain (14.2.0)
- **HDL**: Verilog HDL for RTL, SystemVerilog for the testbench
- **Simulator**: Verilator (v5.033)
- **FPGA synthesis**: Vivado Edition 2024.1
- **Supported boards**:
  - Nexys 4 DDR 100T (DDR2, 128 MB)
  - Arty A7 35T (DDR3, 256 MB)

We develop on Ubuntu 22.04 LTS, and this guide is primarily written for that environment. We have also confirmed operation on Windows 11 Education, but some tools do not provide Windows installers, so WSL2 is required in those cases. Commands in the Makefiles use Unix conventions, so WSL2 is recommended for Windows users. Some tools do not support Arm environments. If you plan to work on Arm hardware, consider using an x86_64 virtual machine.



A Docker-based build environment is also provided. Running `./tools/setup.sh` sets up the container with all simulation tools pre-installed (Vivado must be installed natively). Docker is required; see the [Docker installation guide](https://docs.docker.com/get-docker/) if you do not have it. For details, see [Installation Guide](install.md).



## Verification status

RVComp has been validated in simulation using the following test suites:

- **riscv-tests**: Covers the RISC-V ISA(rv32ui, rv32um, rv32ua, rv32mi, rv32si) (passes all tests except `ma_data`)
- **riscv-arch-test**: Passes every test(RV32IMASUZicntr_Zicsr_Zifencei) when compared against Spike via RISCOF

The `ma_data` test in riscv-tests checks misaligned accesses. Implementing hardware support for this rarely used feature would add significant complexity, so handling it with software exceptions is acceptable. RVComp intentionally raises a software exception instead, which is why the test does not pass. We also boot Linux kernel 6.13.0, run the CoreMark-PRO benchmark in validation mode, and confirm that it produces the expected results.
