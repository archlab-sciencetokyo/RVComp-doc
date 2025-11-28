# RVCpu - RISC-V Processor

## Overview

RVCpu is a 32-bit processor core implementing the RISC-V ISA RV32IMA + Zicsr + Zifencei.
It adopts a 5-stage pipeline structure and supports branch prediction, caches, and privilege modes.
```
cpu (cpu/cpu.v)
 ├── alu (cpu/alu.v)                        # Arithmetic Logic Unit
 ├── bimodal (cpu/bimodal.v)                # Branch predictor
 ├── bru (cpu/bru.v)                        # Branch resolution unit
 ├── csr_regfile (cpu/csr_regfile.v)        # CSR register file
 ├── csralu (cpu/csralu.v)                  # CSR operation ALU
 ├── decoder (cpu/decoder.v)                # Instruction decoder
 ├── divider (cpu/divider.v)                # Divider
 ├── ifu (cpu/ifu.v)                        # Instruction fetch unit
 ├── imm_gen (cpu/imm_gen.v)                # Immediate generator
 ├── lsu (cpu/lsu.v)                        # Load/store unit
 │   ├── amo_decoder (cpu/amo_decoder.v)    # Atomic instruction decoder
 │   └── amoalu (cpu/amoalu.v)              # Atomic operation ALU
 ├── multiplier (cpu/multiplier.v)          # Multiplier
 └── regfile (cpu/regfile.v)                # General-purpose register file
```
### Key Features

- **ISA**: RV32IMA_Zicntr_Zicsr_Zifencei
  - RV32I: Base integer instructions
  - M extension: Multiply/divide instructions
  - A extension: Atomic instructions
  - Zicntr: Counter instructions
  - Zicsr: CSR instructions
  - Zifencei: Instruction fence
- **Privilege Levels**: Machine (M), Supervisor (S), User (U)
- **Pipeline**: 5-stage (IF, ID, OF, EX, WB)
- **Branch Prediction**: Bimodal predictor + BTB
- **Exceptions/Interrupts**: Full support

## Pipeline Structure

The processor adopts a 5-stage pipeline consisting of Instruction Fetch stage (IF), Instruction Decode stage (ID), Operand Fetch stage (OF), Execution stage (EX), and Write Back stage (WB).
An OF stage is added to prevent operating frequency degradation due to CSR access.
To simplify data forwarding, memory access is performed only in the EX stage.

```
+--------+     +--------+     +--------+     +--------+     +--------+
|   IF   | --> |   ID   | --> |   OF   | --> |   EX   | --> |   WB   |
+--------+     +--------+     +--------+     +--------+     +--------+
Instruction    Instruction     Operand       Execution        Write
  Fetch          Decode         Fetch          Stage          Back
```

### 1. IF (Instruction Fetch) Stage
- Instruction address generation
- Instruction fetch
- Branch prediction
- L0 instruction cache access

### 2. ID (Instruction Decode) Stage
- Instruction decode
- Immediate generation
- Exception detection (page fault, access fault during instruction fetch)

### 3. OF (Operand Fetch) Stage
- Register read
- CSR read
- Data forwarding determination
- Interrupt detection
- Exception detection (illegal instruction exception)


### 4. EX (Execution) Stage
- Arithmetic logic operations
- Branch resolution
- Memory address calculation, memory access
- Multiplication/division
- Exception detection (page fault, access fault, misalignment detection during data access)

### 5. WB (Write Back) Stage
- Write back to register file
- Write back to CSR
- Exception/interrupt handling

### Module Description

#### alu (cpu/alu.v)
Arithmetic Logic Unit.
The following optimizations aim to improve operating frequency:
- Path shortening through one-hot encoding control
- Output selection via OR circuit

#### amo_decoder (cpu/amo_decoder.v)
Atomic instruction decoder (A extension).
Decodes the operation type for AMO instructions that perform load-operate-store operations exclusively.

#### amoalu (cpu/amoalu.v)
Atomic operation ALU (A extension).
Performs operations on values read from memory and specified register values.

#### bimodal (cpu/bimodal.v)
Bimodal branch predictor.
Performs branch prediction using a 2-bit counter (Strongly taken/Weakly taken/Weakly untaken/Strongly untaken).
Has a configurable prediction table depth.

#### bru (cpu/bru.v)
Branch resolution unit.
Evaluates branch conditions and determines the correctness of branch predictions.
If the branch prediction is incorrect, the program counter is updated in the WB stage.
A branch prediction miss flushes 4 instructions.

#### csr_regfile (cpu/csr_regfile.v)
CSR (Control and Status Register) register file.
Manages control/status registers such as mstatus, mie, mip, mtvec, mepc, mcause, and satp.
When privilege information is updated, instructions before the WB stage are invalidated and re-executed, as permission checks during instruction fetch may be incorrect at that point.
When a data hazard occurs on a CSR, instructions before the OF stage are also invalidated and re-executed.

#### csralu (cpu/csralu.v)
CSR operation ALU.
Computes values to write to CSRs or general-purpose registers via CSR instructions.

#### decoder (cpu/decoder.v)
Instruction decoder.
Analyzes instructions and generates control signals.
Also performs illegal instruction detection.

#### divider (cpu/divider.v)
Divider (M extension).
Uses a simple division algorithm.
Takes 34 cycles to compute and stalls for 33 cycles.

#### ifu (cpu/ifu.v)
Instruction fetch unit.
Fetches instructions from the address pointed to by the program counter.


Contains an internal L0 instruction cache.
The L0 instruction cache has several optimizations to reduce latency.
The L0 instruction cache is implemented with Virtually Tagged, Virtually Indexed to reduce address translation latency.
Due to the VIVT approach, hardware countermeasures are needed if making it larger than 4KiB.
It uses direct-mapped organization with a block size of 16 Bytes.
L0 instruction cache data and tags are implemented using LUTRAM. This divides the path and aims to improve operating frequency.
If making it larger than 1 KiB, operating frequency may decrease significantly due to LUTRAM constraints.

The L0 instruction cache valid bit is implemented with registers. This allows it to be flushed in 1 cycle.
The L0 instruction cache is flushed in the following cases:
- When privilege information is updated
- When fence.i instruction is executed (instruction to synchronize with main memory, ensuring instruction cache contents are up-to-date)
- When sfence.vma instruction is executed (instruction to synchronize with memory management structures, ensuring TLB contents are up-to-date)
#### imm_gen (cpu/imm_gen.v)
Immediate generator.
Extracts immediates from I/S/B/U/J format instructions and performs appropriate sign extension and shifting.

#### lsu (cpu/lsu.v)
Load/store unit.
Responsible for memory access control, alignment checking, and atomic instruction execution.
Sign extension and zero extension are also performed in this module.
AMO instruction control is also handled by this module.
Due to single-core design, AMO instruction exclusivity is realized through state transitions.

#### multiplier (cpu/multiplier.v)
Multiplier (M extension).
Takes 3 cycles to compute and stalls for 2 cycles.

#### regfile (cpu/regfile.v)
General-purpose register file (x0-x31).
Has 2 read and 1 write port, and x0 always returns 0.
