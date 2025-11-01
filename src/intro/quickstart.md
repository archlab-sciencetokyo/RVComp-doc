# Quick Start

This section explains how to run RVComp on an FPGA board using a prebuilt bitstream and Linux image. 
Please Download the following files from [the release page](https://github.com/archlab-sciencetokyo/RVComp/releases).
- `fw_payload.bin`: Linux image file
- `arty_a7.bit`: Bitstream for Arty A7 35T FPGA board
- `nexys4ddr.bit`: Bitstream for Nexys 4 DDR FPGA
- `tools.zip` : Programs to communicate with the FPGA board via UART.
Please unzip `tools.zip`.

Please make sure the necessary tools and the FPGA board are ready:
- {ref}`Vivado (2024.1 recommended) <vivado>`
- {ref}`uv <uv>`
- FPGA board (Nexys 4 DDR or Arty A7 35T)

Guidance for WSL2 usage will be added to this section later.

1. Please connect the FPGA board to your PC.
2. Please download and extract `fw_payload.bin`, `arty_a7.bit` (for Arty A7 35T), `nexys4ddr.bit` (for Nexys 4 DDR), and the `tools` directory from the archive mentioned above, and place them in the same directory.
3. Please determine which serial port the USB connection is using. See [Checking the Serial Port](#checking-the-serial-port) below.
4. Please open PowerShell (Windows) or a terminal (Linux) and change to the directory from step 2.
5. Please run the following command, replacing `<port>` with the value from step 3. On success you should see `Port <port> opened successfully.`.
   - Nexys 4 DDR: `cd tools && uv run term <port> 3200000 --linux-boot --linux-file-path ../image/fw_payload.bin`
   - Arty A7 35T: `cd tools && uv run term <port> 3300000 --linux-boot --linux-file-path ../image/fw_payload.bin`
6. Please launch Vivado and select **Open Hardware Manager → Open Target → Auto Connect → Program Device**.
7. When prompted for the bitstream, please choose `arty_a7.bit` if you use Arty A7, or `nexys4ddr.bit` if you use Nexys 4 DDR, then click **Program**.
8. The Linux image is transferred to the FPGA and boot begins. Once the login prompt appears, please log in as `root` (no password).
9. Please press `Ctrl+C`, then type `:q` to exit the serial console.

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
