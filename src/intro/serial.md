# Using RVComp on FPGA with the Serial Program

This page explains how to operate RVComp after generating the bitstream and how to use the bundled serial communication tool. Please install the required software beforehand (see the [Installation Guide](install.md)).

- {ref}`Vivado <vivado>`
- {ref}`uv <uv>`

## Serial communication with the FPGA

For a locally connected FPGA, after completing the [Makefile setup](makesetup.md) (Vivado path and `COM_PORT`), please run `$ make term` to start the serial program. Please open another terminal and run `$ make config` to load the bitstream and send the Linux image automatically.

To operate the tool manually:

1. Please identify the serial port connected to the FPGA. See [Communication Port Check](#communication-port-check).
2. Please edit `config.mk` and set `COM_PORT` to the port name you found.
3. Please run `$ make term` to launch the serial communication program.
4. Please load the bitstream onto the FPGA (see [Load to FPGA](#load-to-fpga)). If the console does not display anything, refer to [Troubleshooting](#troubleshooting).
5. The terminal shows `[     bootrom] Hello, world!`.
6. Please open another terminal and run `cat image/fw_payload.bin > <port>` to send the Linux image.
7. Once the transfer completes, Linux boots and the login prompt appears. If it does not boot correctly, please refer to [Troubleshooting](#troubleshooting).
8. Please press `Ctrl+C`, then type `:q` to close the serial program.

(load-to-fpga)=
## Load to FPGA

### Local FPGA

If you use the Vivado GUI, please start Vivado and choose **Open Hardware Manager → Open Target → Auto Connect** to connect. Then select **Program Device**, choose the generated bitstream, and program the FPGA.

After completing the [Makefile setup](makesetup.md) (Vivado path), you can load the bitstream with:

```bash
$ make load
```

### Remote FPGA

Please start the Hardware Server that matches your Vivado version on the PC connected to the FPGA board. In the Vivado GUI, please choose **Open Hardware Manager → Open Target → Connect to Remote Server**, enter the IP address and port (the default port is usually fine), and connect. Then select **Program Device** and load the bitstream.

After configuring the Vivado path, IP address, and device serial number in [Makefile setup](makesetup.md), you can load the remote FPGA with:

```bash
$ make remoteload
```

(troubleshooting)=
## Troubleshooting

### `[     bootrom] Hello, world!` does not appear

- The bitstream was not loaded onto the FPGA.
- Serial port settings (port, encoding, baud rate, etc.) are incorrect.
- Bad physical connection. Please try reseating or replacing the cable, or using another USB port.
- The bitstream was generated without rebuilding the bootrom image. Please run `make bootrom` first to create `bootrom.128.hex`, then regenerate the bitstream.
- Communication still fails even though settings look correct:
  - Very high baud rates can fail due to device or terminal limitations.
  - RVComp matches the baud rate by waiting `floor(Clock Frequency (Hz) / Baudrate (bps))` cycles. If the truncation error is large, communication can fail. Please adjust the clock frequency or baud rate to reduce the error.

### Linux image was sent but Linux does not boot

- If the console output becomes garbled, the serial link is likely the problem. Please follow the same checks as above.
- You typed something in the serial console after launching the program. RVComp counts the bytes arriving over UART and writes them to DRAM before running the second-stage bootloader. Extra input corrupts the count. Please reload the bitstream and resend the Linux image.
- The bitstream was generated without a proper bootrom image:
  - The bootrom needs the byte length of the incoming binary. Please verify the `BIN_SIZE` argument passed to `make bootrom` in `config.mk` (it should match the size of `images/fw_payload.bin`) and regenerate the bitstream.
  - The bootrom must be 8 KiB or smaller. If it exceeds 8 KiB, please modify the program or increase `ROM_SIZE` in the bootrom module.
- The console stops at the OpenSBI banner. The transferred binary may not include a Linux image. Refer to [Building Linux](build.md).

(communication-port-check)=
## Communication Port Check

Use these steps to identify the serial port assigned to the FPGA. The simplest approach is to compare the device list before and after unplugging the FPGA.

### Windows

Please run the following command in PowerShell:

```powershell
Get-CimInstance Win32_PnPEntity | Where-Object { $_.Caption -match 'COM' } | Select-Object Caption, DeviceID
```

Please find the device whose `DeviceID` contains `FTDI`; it corresponds to the FPGA board and appears as `USB Serial Device (COM*)`. Please note the COM port name.

### WSL

Please follow [Microsoft’s instructions](https://learn.microsoft.com/en-us/windows/wsl/connect-usb) to attach USB devices to WSL. The entry with `VID:PID` of `0403:6010` reported by `usbipd list` is typically the FPGA. After attaching it, please follow the Linux procedure below.

### Linux

Please run:

```bash
$ ls /dev/ttyUSB*
```

The command lists USB serial devices. If only the FPGA is connected, it is usually `/dev/ttyUSB1`. When multiple devices exist, please run:

```bash
$ udevadm info /dev/ttyUSB1 | grep ID_VENDOR=
```

Please look for a device whose vendor is Digilent, and please record the corresponding `/dev/ttyUSB*` path.

## Serial communication program

Our FPGA serial communication application uses `pyserial`. It opens the port and handles transmit and receive in separate threads. Dependencies are managed with `uv`, so please install `uv` beforehand.

Please run the tool directly with:

```bash
$ cd tools
$ uv run term <port> <baudrate> [options]
```

Running `make term` is equivalent, but it enables automatic Linux boot and does not require changing directories.

Most `pyserial` settings are exposed as command‑line options. Please press `Ctrl+C`, then `:q` to exit the program.

```
usage: term [-h] [-b {5,6,7,8}] [-p {N,E,O,M,S}] [-s {1,1.5,2}] [-r] [-x] [-d]
            [-w WRITE_TIMEOUT] [-i INTER_BYTE_TIMEOUT] [-f LINUX_FILE_PATH] [-l]
            [--bitstream-load {None,local,remote}]
            port baudrate

Serial port terminal communication tool

positional arguments:
  port                  Serial port device (e.g., /dev/ttyUSB0, COM1)
  baudrate              Baud rate (e.g., 9600, 115200)

options:
  -h, --help            show this help message and exit
  -b {5,6,7,8}, --bytesize {5,6,7,8}
                        Number of data bits
  -p {N,E,O,M,S}, --parity {N,E,O,M,S}
                        Parity check: N=NONE, E=EVEN, O=ODD, M=MARK, S=SPACE
  -s {1,1.5,2}, --stopbits {1,1.5,2}
                        Number of stop bits
  -r, --rtscts          Enable RTS/CTS hardware flow control
  -x, --xonxoff         Enable XON/XOFF software flow control
  -d, --dsrdtr          Enable DSR/DTR hardware flow control
  -w WRITE_TIMEOUT, --write-timeout WRITE_TIMEOUT
                        Write timeout in seconds
  -i INTER_BYTE_TIMEOUT, --inter-byte-timeout INTER_BYTE_TIMEOUT
                        Inter-byte timeout in seconds
  -f LINUX_FILE_PATH, --linux-file-path LINUX_FILE_PATH
                        Relative path of the Linux image to send
  -l, --linux-boot      Linux boot mode: send the Linux image after detecting the loader
  --bitstream-load {None,local,remote}
                        Bitstream load method (local or remote)

commands:
   Ctrl+C -> :q         Exit the program
```
