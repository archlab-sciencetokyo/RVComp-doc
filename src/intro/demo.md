# Demo

A camera streaming demo running on RVComp. Source code is available in the [`feature/v1.1.0-demo`](https://github.com/archlab-sciencetokyo/RVComp/tree/feature/v1.1.0-demo) branch of the [RVComp](https://github.com/archlab-sciencetokyo/RVComp) repository.

## Overview

This demo uses an [OV7670 (OmniVision)](https://www.ovt.com/press-releases/omnivision-launches-seventh-generation-vga-camerachip-for-mobile-applications/) camera module connected to a Nexys 4 DDR board. The camera captures 320×240 frames, converts them to 8-bit grayscale on the FPGA, and transmits them to a host PC over Ethernet. The demo runs on a local network (LAN).

```
OV7670 → FPGA (Gray8 capture) → Linux (cam_tx, UDP) → Host (relay.py, WebSocket) → Browser
```

## Demo Video

The demo is filmed in a bright indoor environment. Because frames are encoded as 8-bit grayscale, good ambient lighting improves image quality.

```{raw} html
<video width="100%" controls>
  <source src="../_static/media/demo.mp4" type="video/mp4">
</video>
```

## Running the Demo

### On RVComp (Linux)

After booting Linux, assign an IP address and bring up the Ethernet interface:

```sh
$ ip addr add <IP_ADDRESS>/<PREFIX_LEN> dev eth0
$ ip link set eth0 up
```

Then start the camera transmitter:

```sh
$ cam_tx --host <HOST_IP_ADDRESS>
```

```
Usage: cam_tx [--dev PATH] [--host IP] [--port N] [--payload N]
Defaults: --dev /dev/rvcomp_cam0 --host 192.168.0.2 --port 5000 --payload 1200
```

### On the Host PC

Run `relay.py` from `tools/camera/` using `uv`:

```sh
$ cd tools/camera
$ uv run relay.py --port 5000 --ws-port 8000
```

Then open `http://localhost:8000` in a browser to view the live camera stream.

```
usage: relay.py [-h] [--udp-host UDP_HOST] [--udp-port UDP_PORT] [--ws-host WS_HOST] [--ws-port WS_PORT]

RVComp camera relay

options:
  -h, --help            show this help message and exit
  --udp-host UDP_HOST   UDP bind host
  --udp-port UDP_PORT   UDP bind port
  --ws-host WS_HOST     HTTP/WS bind host
  --ws-port WS_PORT     HTTP/WS bind port
```

## System Configuration

### External Pins

The OV7670 is connected to the PMOD JA and JB headers on the Nexys 4 DDR board.

| Signal            | Direction | Description |
|:------------------|:----------|:------------|
| `xclk`            | Output    | Camera input clock (25 MHz) |
| `pclk`            | Input     | Pixel clock |
| `camera_h_ref`    | Input     | Horizontal sync |
| `camera_v_sync`   | Input     | Vertical sync |
| `din[7:0]`        | Input     | 8-bit pixel data |
| `sioc`            | Output    | I2C clock (SCCB) |
| `siod`            | Inout     | I2C data (SCCB) |

### Camera Driver

An FPGA block captures frames from the OV7670 via I2C (SCCB). Pixel data is converted to 8-bit grayscale and stored in two frame buffers in BRAM (ping-pong). 8-bit grayscale was chosen because fitting two full-resolution color frame buffers in BRAM would exceed the available capacity.

A Linux misc driver (`rvcomp-camera`) exposes the device as `/dev/rvcomp_cam0`. The driver accesses the camera hardware via MMIO polling (no IRQ). It supports `read`, `poll`, and `ioctl` (`RVCOMP_CAM_IOC_G_INFO`, `RVCOMP_CAM_IOC_G_META`).

#### MMIO Map

| Region         | Start         | End           | Description |
|:---------------|:-------------:|:-------------:|:------------|
| CSR            | `0xB000_0000` | `0xB000_0FFF` | Control and status registers |
| Frame aperture | `0xB001_0000` | `0xB002_FFFF` | Ping-pong frame buffer window |

#### CSR Map

All CSRs are 32-bit wide.

| Offset | Name               | Access | Description |
|:------:|:-------------------|:------:|:------------|
| 0x00   | `CAM_REG_ID`       | R      | Device ID |
| 0x04   | `CAM_REG_CTRL`     | R/W    | Control (bit 0: capture enable) |
| 0x08   | `CAM_REG_STATUS`   | R      | Status |
| 0x0C   | `CAM_REG_WIDTH`    | R      | Image width in pixels |
| 0x10   | `CAM_REG_HEIGHT`   | R      | Image height in pixels |
| 0x14   | `CAM_REG_STRIDE`   | R      | Row stride in bytes |
| 0x18   | `CAM_REG_FRAME_BYTES` | R   | Total frame size in bytes |
| 0x1C   | `CAM_REG_SEQ`      | R      | Frame sequence counter |
| 0x20   | `CAM_REG_READY_BANK` | R    | Bank holding the latest complete frame |
| 0x24   | `CAM_REG_READ_BANK`  | R/W  | Bank selected for readout |
| 0x28   | `CAM_REG_DROP_COUNT` | R    | Number of dropped frames |
| 0x2C   | `CAM_REG_GAIN`     | R/W    | Gain control |

### Transmission Program (`cam_tx`)

`cam_tx` is a userspace program that reads frames from `/dev/rvcomp_cam0` and transmits them to the host as UDP datagrams. Each frame is split into chunks with a custom header (`RVCP` magic, sequence number, width, height, chunk index/count) to allow reassembly on the host.

### Client Program (`relay.py`)

`relay.py` runs on the host and acts as a relay between `cam_tx` and the browser. It listens for UDP datagrams from `cam_tx`, reassembles the frame chunks, and broadcasts each completed frame to all connected WebSocket clients. The browser connects to the WebSocket endpoint (`/ws`) and renders each frame on an HTML5 Canvas element.

## Going Further

The current implementation uses CPU-driven (PIO) reads from the BRAM frame buffer and UDP transmission, which limits the achievable frame rate.

Since this runs on an FPGA, the hardware is fully reconfigurable. For example:

- **DMA**: offload frame readout from the CPU entirely
- **FPGA-side Ethernet framing**: generate UDP/IP headers in hardware and push frames to the MAC without CPU involvement
- **Pipeline**: overlap capture and transmission in the FPGA fabric

Changes that would require a full chip respin on an ASIC can be explored here simply by modifying the RTL — feel free to experiment.
