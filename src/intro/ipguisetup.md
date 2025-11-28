# IP Setup (GUI)

## Overview
RVComp uses AMD's Clocking Wizard and MIG (Memory Interface Generator) as IP. These IPs can be generated from Vivado's GUI.

Clocking Wizard is an IP core for generating clocks at target frequencies from input clocks using FPGA clock management tiles.

MIG (Memory Interface Generator) is an IP core provided by AMD for controlling DDR2/DDR3 SDRAM on FPGA. The MIG GUI can be used to generate DRAM controllers tailored to the target FPGA device.

## MIG (Nexys4DDR 100T)
1. Search for "Memory Interface Generator" from "IP Catalog" and double-click to add the IP.
2. The "Customize IP" window opens. Configure the following settings:
3. Click Next.
4. Configure the following items and click Next.
   - AXI4 Interface: Checked
5. Click Next.
6. Configure the following items and click Next.
   - Memory Selection: DDR2 SDRAM
7. Configure the following items and click Next.
   - Memory Part: MT47H64M16GR-25E
   - Data Width: 16
8. Click Next.
9. Configure the following items and click Next.
   - Input Clock Period: 6000 ps (166.667 MHz)
   - RTT (nominal) - ODT: 50ohms
10. Configure the following items and click Next.
    - System Clock: No Buffer
    - Reference Clock: No Buffer
    - System Reset Polarity: ACTIVE HIGH
    - Internal Vref: Checked
11. Click Next.
12. Configure the following items and click Next.
    - Fixed Pin Out: Checked
13. Click Read XDC/UCF, select rvcomp/constr/Nexys-Mig.ucf and click OK. Then click Validate, click OK, and then click Next.
14. Click Next.
15. Click Next.
16. After reviewing the simulation model license agreement, click Accept and click Next.
17. Click Next.
18. Click Generate.
19. Click Generate to finish.

## MIG (Arty A7 35T)
1. Search for "Memory Interface Generator" from "IP Catalog" and double-click to add the IP.
2. The "Customize IP" window opens. Configure the following settings.
3. Click Next.
4. Configure the following items and click Next.
   - AXI4 Interface: Checked
5. Click Next.
6. Configure the following items and click Next.
   - Memory Selection: DDR3 SDRAM
7. Configure the following items and click Next.
   - Clock Period: 3,000 ps (333.333 MHz)
   - Memory Part: MT41K128M16XX-15E
   - Memory Voltage: 1.35V
   - Data Width: 16
8. Click Next.
9. Configure the following items and click Next.
   - Input Clock Period: 6000 ps (166.667 MHz)
   - Output Driver Impedance Control: RZQ/6
   - RTT (nominal) - On Die Termination(ODT): RZQ/6
10. Configure the following items and click Next.
    - System Clock: No Buffer
    - Reference Clock: No Buffer
    - System Reset Polarity: ACTIVE HIGH
    - Internal Vref: Checked
11. Click Next.
12. Configure the following items and click Next.
    - Fixed Pin Out: Checked
13. Click Read XDC/UCF, select rvcomp/constr/Arty-Mig.ucf and click OK. Then click Validate, click OK, and then click Next.
14. Click Next.
15. Click Next.
16. After reviewing the simulation model license agreement, click Accept and click Next.
17. Click Next.
18. Click Generate.
19. Click Generate to finish.


## Clocking Wizard

### clk_wiz_1 (for DRAM Controller)
1. Search for "Clocking Wizard" from "IP Catalog" and double-click to add the IP.
2. The "Customize IP" window opens. Configure the following settings.
3. Click "Clocking Options".
4. Check "Minimize Output Jitter".
5. Click "Output Clocks".
6. Congiure the following and click OK.
    - check clk_out2
    - Request of clk_out1's Output Freq (MHz): 166.6666 
    - Request of clk_out1's Output Freq (MHz): 200.0000

### clk_wiz_2 (for SoC)
1. Search for "Clocking Wizard" from "IP Catalog" and double-click to add the IP.
2. The "Customize IP" window opens. Configure the following settings.
3. Click "Clocking Options".
4. Check "Minimize Output Jitter".
5. Click "Output Clocks".
6. Congiure the following and click OK.
    - Request of clk_out1's Output Freq (MHz): (SoC's clock freqency, default=160)