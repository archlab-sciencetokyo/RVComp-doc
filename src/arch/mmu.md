# MMU - Memory Management Unit

## Overview

The MMU (Memory Management Unit) is a module responsible for virtual memory management, address translation, and L1 cache control.
It supports RISC-V SV32 (Supervisor Virtual Memory 32-bit) and implements a page-based virtual memory system.
```
mmu (mmu/mmu.v)
├── dtlb (mmu/dtlb.v)                      # Data TLB
├── itlb (mmu/itlb.v)                      # Instruction TLB
├── l1_dcache (cache/l1_dcache.v)          # L1 data cache
├── l1_icache (cache/l1_icache.v)          # L1 instruction cache
└── ptw (mmu/ptw.v)                        # Page table walker
```

## Key Features

- **Address Translation**
- **Address Protection**
- **L1 Cache Control**
- **Lower Memory Access**
- **Store-Conditional (SC) Instruction Support**


## MMU (mmu/mmu.v)
Processes instruction and data read/write requests in parallel.
The MMU is managed through the following 3 state machines:
- Instruction memory access
- Data memory access
- Lower memory access

The general flow is as follows:
Instruction (I_CTRL):
1. Receive instruction fetch request from CPU
2. Translate virtual address to physical address in ITLB, fetch PTE from lower memory under PTW control on miss, check permission information
3. If page fault exception or access fault exception is detected, return exception information to CPU
4. Check cache hit in L1 I-Cache, fetch from lower memory on miss
5. If access fault exception is detected, return exception information to CPU
6. Return instruction to CPU

Data (D_CTRL):
1. Receive load/store request from CPU
2. Translate virtual address to physical address in DTLB, fetch PTE from lower memory under PTW control on miss, check permission information
3. If page fault exception or access fault exception is detected, return exception information to CPU
4. For Store-Conditional instructions, compare with reservation address and execute store only if condition is met, return to CPU if failed
5. For peripheral access, send access request to lower memory and wait for response
6. Check cache hit in L1 D-Cache, load from lower memory on miss and execute load/store
7. Return data to CPU

Lower Memory (M_CTRL):
1. Receive PTW's PTE fetch requests and L1 I/D-Cache miss access requests, process from highest priority if multiple
2. Before accessing upper cache, check if the address to access exists in L1 D-Cache and check Dirty bit, write back to lower memory first if Dirty
3. Access lower memory and obtain data
4. Notify completion, notify exception information if exception occurs

## TLB (mmu/itlb.v, mmu/dtlb.v)
TLB (Translation Lookaside Buffer) is a cache to accelerate translation from virtual addresses to physical addresses.
There are two TLBs: ITLB (Instruction TLB) and DTLB (Data TLB).

Direct-mapped organization is adopted to achieve high operating frequency and low latency.
TLBs generally adopt set-associative or fully-associative methods because address space locality is low.
We adopted direct-mapped organization, prioritizing latency and operating frequency.
Instead, to increase hit rate, we recommend using more entries than usual.
Implementing TLB data and tags in BRAM secures many entries while suppressing hardware resource increase.

On miss, PTW (Page Table Walker) references the page table, obtains PTE (Page Table Entry), and writes to TLB.
TLB entries are as follows:
```
TLB ENTRY:
┌─────────┬──────────────────────┬──────────────┐
│ Lvl (1) │ Tag (32-INDEX_WIDTH) │ PTE (32)     │
└─────────┴──────────────────────┴──────────────┘
```

## PTW (mmu/ptw.v)
PTW (Page Table Walker) is a hardware module that references the page table on TLB miss and obtains PTE (Page Table Entry).
Since SV32 allows 2-level page table walk, PTW performs up to 2 memory accesses per PTE.
Lower memory access is performed through the MMU's state machine.

## L1 Cache (cache/l1_icache.v, cache/l1_dcache.v)
The MMU includes an L1 instruction cache and L1 data cache.
The common parts of the L1 cache are explained first, followed by the differences between each cache.

The L1 cache adopts the PIPT (Physically Indexed, Physically Tagged) method, which uses physical addresses for cache index and tag.
Using physical addresses prevents synonym and alias problems that occur when using virtual addresses.
This allows simple scalability to large capacity.
It uses direct-mapped organization with a block size of 16 Bytes.
These methods increase hit rate while maintaining high operating frequency and reducing latency.

In the current implementation, to shorten paths, the L1 cache uses the lower 12 bits of the virtual address for the index and the 22 bits of the physical address obtained from TLB or PTW for the tag.
Therefore, if making it smaller than 8 KiB, the Verilog HDL code needs to be modified.

### L1 Instruction Cache
The L1 instruction cache is updated only when fetching from lower memory on cache miss.
To maintain consistency, when a store instruction is executed on an entry in the L1 instruction cache, that entry is invalidated.

```
Meta RAM:
┌──────────┬─────────────────┐
│ valid(1) │ tag(TAG_WIDTH)  │
└──────────┴─────────────────┘

Data RAM:
┌─────────────────────────────┐
│ data (128)                  │
└─────────────────────────────┘
```

### L1 Data Cache
The L1 data cache adopts Write-back and Write-allocate policies.
When a store instruction hits the cache, it updates the data in the cache and sets the Dirty bit.
On cache miss, it loads data from lower memory and writes to the cache line.

```
Meta RAM:
┌──────────┬───────────┬─────────────────┐
│ valid(1) │ dirty(1)  │ tag(TAG_WIDTH)  │
└──────────┴───────────┴─────────────────┘

Data RAM:
┌─────────────────────────────┐
│ data (128)                  │
└─────────────────────────────┘
```

## MMU State Machines

The operation of each state is as follows:

### Instruction Fetch Control (istate_q)
| State    | Operation                       |
|----------|---------------------------------|
| `I_IDLE` | Wait for instruction fetch request |
| `I_TLB`  | ITLB reference                  |
| `I_CACHE`| L1 I-Cache access               |
| `I_PTW`  | Page table walk                 |
| `I_FETCH`| Fetch from lower memory         |
| `I_RET`  | Return response to CPU          |

### Data Load/Store Control (dstate_q)

| State      | Operation                       |
|------------|---------------------------------|
| `D_IDLE`   | Wait for load/store request     |
| `D_TLB`    | DTLB reference                  |
| `D_CACHE`  | L1 D-Cache access               |
| `D_PTW`    | Page table walk                 |
| `D_RET`    | Return response to CPU          |
| `D_CHECK`  | LR/SC condition check           |
| `D_STORE`  | Execute store                   |
| `D_ALLOCATE`| Load from lower memory         |
| `D_PERIPH` | Peripheral access               |

### Lower Memory Control (mstate_q)

| State    | Operation                   |
|----------|-----------------------------|
| `M_IDLE` | Wait for read/write request |
| `M_PTW`  | PTW's PTE fetch             |
| `M_DCHECK`| Dirty line check           |
| `M_WRITE`| Execute write-back          |
| `M_READ` | Read from lower memory      |
