# Setup Before Make Command

This section describes the configuration required before running the Make targets. Environment-specific settings live in `config.mk`, which is included from the main Makefile. Please use the provided template and define the variables below.

## For FPGA

### Serial communication

Please configure these variables to use the serial communication program through the Make targets:

- `COM_PORT`  
  Specify the device file for the FPGA board’s serial port (for example, `/dev/ttyUSB0`).

### Synthesis and implementation

Please set the following variables to run logic synthesis, place-and-route, and bitstream generation via Make:

- `vivado`  
  Path to the Vivado executable. You can omit this if Vivado is already in `PATH`. Use an absolute path otherwise.
- `board_data_path`  
  Absolute path to the Xilinx Board Files.
- `RISCV_PATH`  
  Installation path of the riscv-gnu-toolchain GCC (up to `bin/`). Include the trailing slash. If `riscv32-unknown-elf-gcc` is already in `PATH`, you can leave this unset.
- `serial_number` (for `remoteload` only)  
  Serial number of the FPGA board when loading through the Vivado hardware server.
- `ip_address` (for `remoteload` only)  
  IP address of the host that runs the hardware server.

Please update these variables whenever you change the Linux image or boot payload:

- `BIN_SIZE`  
  Size of the Linux image in bytes (`Size` reported by `stat <file>`). Keep it in sync with the payload you send.
- `linux_image`  
  Absolute path to the Linux image transferred over the serial link after loading the bitstream.
