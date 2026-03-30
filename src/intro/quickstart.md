# Quick Start

This section explains how to run RVComp on an FPGA board using a prebuilt bitstream and Linux image.


Please download the following files from [the release page](https://github.com/archlab-sciencetokyo/RVComp/releases).

**UART boot (Arty A7 35T or Nexys 4 DDR):**
- `uart_fw_payload.bin`: Linux image file for UART boot
- `uart_arty_a7.bit`: Bitstream for Arty A7 35T (UART boot)
- `uart_nexys4ddr.bit`: Bitstream for Nexys 4 DDR (UART boot)

**MMC boot (Nexys 4 DDR only):**
- `mmc_fw_payload.bin`: Linux image for MMC boot
- `mmc_nexys4ddr.bit`: Bitstream for Nexys 4 DDR (MMC boot)

```{note}
MMC boot requires a microSD card inserted into the Nexys 4 DDR board's microSD slot.
If an Ethernet cable is connected to the board, the network interface is available after boot.
```

**Common:**
- `tools.zip`: Programs to communicate with the FPGA board via UART

Please unzip `tools.zip`.

Please make sure the necessary tools and the FPGA board are ready:
- {ref}`Vivado (2024.1 recommended) <vivado>`
- {ref}`uv <uv>`
- FPGA board (Nexys 4 DDR or Arty A7 35T)





## UART Boot (Arty A7 35T or Nexys 4 DDR)

1. Please connect the FPGA board to your PC.
2. Please download and extract `uart_fw_payload.bin`, `uart_arty_a7.bit` (for Arty A7 35T) or `uart_nexys4ddr.bit` (for Nexys 4 DDR), and the `tools` directory from the archive mentioned above, and place them in the same directory.
3. Please determine which serial port the USB connection is using. See [Checking the Serial Port](#checking-the-serial-port) below.
4. Please open PowerShell (Windows) or a terminal (Linux) and change to the directory from step 2.
5. Please run the following command, replacing `<port>` with the value from step 3. On success you should see `Port <port> opened successfully.`.
   - Nexys 4 DDR: `cd tools && uv run term <port> 3000000 --linux-boot --linux-file-path ../uart_fw_payload.bin`
   - Arty A7 35T: `cd tools && uv run term <port> 3000000 --linux-boot --linux-file-path ../uart_fw_payload.bin`
6. Please launch Vivado and select **Open Hardware Manager → Open Target → Auto Connect → Program Device**.
7. When prompted for the bitstream, please choose `uart_arty_a7.bit` if you use Arty A7, or `uart_nexys4ddr.bit` if you use Nexys 4 DDR, then click **Program**.
8. The Linux image is transferred to the FPGA and boot begins. Once the login prompt appears, please log in as `root` (no password).
9. To use Ethernet, configure the network interface:
   ```sh
   $ ip addr add <IP_ADDRESS>/<PREFIX_LEN> dev eth0
   $ ip link set eth0 up
   ```
10. Please press `Ctrl+C`, then type `:q` to exit the serial console.





## MMC Boot (Nexys 4 DDR only)

MMC boot on Nexys 4 DDR requires a microSD card. The `mmc_fw_payload.bin` file is a combined binary containing the Linux image and root filesystem; it is written to the beginning of the microSD card. The serial terminal is still used as a console, but it does not send the Linux image in this mode.

### Writing the microSD card

Insert a microSD card into your host machine.

**Linux:**

Identify the block device node with `lsblk` or `dmesg`. **Verify the device node carefully before proceeding; writing to the wrong device will permanently destroy data on that device.**

```bash
$ sudo dd if=mmc_fw_payload.bin of=/dev/sdX bs=1M conv=fsync,notrunc status=progress
```

Replace `/dev/sdX` with the actual device node of your microSD card (for example `/dev/sdb`). After the command completes, safely eject the card.

**Windows (WSL):**

Attach the microSD card to WSL, then use the same `dd` command as Linux above.

- USB microSD card reader: follow [this guide (usbipd)](https://learn.microsoft.com/en-us/windows/wsl/connect-usb) to bind the device to WSL.
- Built-in card reader: follow [this guide (WSL2 disk mounting)](https://learn.microsoft.com/en-us/windows/wsl/wsl2-mount-disk) to mount the disk in WSL.

### Booting from microSD card

1. Insert the written microSD card into the microSD slot on the Nexys 4 DDR board.
2. Connect the board to your PC via USB.
3. Determine the serial port as described in [Checking the Serial Port](#checking-the-serial-port).
4. Open a terminal and run the following command. No `--linux-boot` flag is **needed** because the serial tool is used only as a console in this mode:
   ```bash
   $ cd tools && uv run term <port> 3000000
   ```
5. Launch Vivado and program the board with `mmc_nexys4ddr.bit` using **Open Hardware Manager → Open Target → Auto Connect → Program Device**.
6. The bootrom copies the Linux image from the microSD card into DRAM and boots Linux. The root filesystem on the microSD card is mounted as `/dev/mmcblk0`. Once the login prompt appears, log in as `root` (no password).
7. To use Ethernet, configure the network interface:
   ```sh
   $ ip addr add <IP_ADDRESS>/<PREFIX_LEN> dev eth0
   $ ip link set eth0 up
   ```
8. Press `Ctrl+C`, then type `:q` to exit the serial console.



(checking-the-serial-port)=
## Checking the Serial Port

### Windows

Please run the following command in PowerShell:

```powershell
Get-CimInstance Win32_PnPEntity | Where-Object { $_.Caption -match 'COM' } | Select-Object Caption, DeviceID
```

Please identify the entry whose `DeviceID` contains `FTDI`; this corresponds to the FPGA board. It appears in the form `USB Serial Device (COM*)`. Please note the COM port name.

### WSL

Please follow the instructions in [this article](https://learn.microsoft.com/en-us/windows/wsl/connect-usb) to attach USB devices to WSL. Please run `usbipd list`; the entry with `VID:PID` of `0403:6010` is usually the FPGA board. After attaching it, please follow the Linux instructions below.

### Linux

Please run the following command in a terminal:

```bash
$ ls /dev/ttyUSB*
```

The available USB serial ports are listed. If only one FPGA board is connected as a USB serial device, it is typically `/dev/ttyUSB1`. When multiple USB serial devices are present, please run the command below for each port and look for a device where `ID_VENDOR` is `Digilent`:

```bash
$ udevadm info /dev/ttyUSB1 | grep ID_VENDOR=
```

Please record the `/dev/ttyUSB*` path assigned to the FPGA board.


## Prebuilt Bitstream Parameters
The prebuilt bitstreams provided in the release are configured with the default settings in `tools/setting.py`.
