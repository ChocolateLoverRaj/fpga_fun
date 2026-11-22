# top = th

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge
from spade import SpadeExt


@cocotb.test()
async def simple_test(dut):
    s = SpadeExt(dut)
    clk = dut.clk
    sda = dut.sda_inv
    scl = dut.scl_inv

    # 1. Start 10 MHz clock (100 ns period) and pull-ups
    cocotb.start_soon(Clock(clk, 100, units="ns").start())

    s.i.rst = False
    s.i.sda = True
    s.i.scl = True

    # The target waits for SDA to go low
    await FallingEdge(sda)
    await FallingEdge(scl)

    byte = 0
    for _ in range(8):
        await RisingEdge(scl)
        byte <<= 1
        byte |= bool(sda.value)

    addr = byte >> 1
    read_write = bool(byte & (1 << 7))

    assert addr == 0x3C
    assert read_write == 0

    await FallingEdge(scl)
    # Pull SDA low to indicate ACK
    s.i.sda = False

    await FallingEdge(scl)
    # Release SDA
    s.i.sda = True

    # Receive data
    expected_bytes = [
      0x00,                               # Control byte: command stream
      0xAE,                               # Display OFF
      0xD5, 0x80,                         # Clock divide / oscillator frequency
      0xA8, 0x3F,                         # Multiplex ratio (64 rows for 128x64)
      0xD3, 0x00,                         # Display offset (0)
      0x40,                               # Display start line (0)
      0x8D, 0x14,                         # Enable internal charge pump (crucial for SSD1306!)
      0x20, 0x00,                         # Horizontal addressing mode
      0xA1,                               # Segment re-map (col 127 -> SEG0)
      0xC8,                               # COM scan direction (remapped)
      0xDA, 0x12,                         # COM pins hardware config (0x12 for 128x64; 0x02 for 128x32)
      0x81, 0xCF,                         # Contrast control
      0xD9, 0xF1,                         # Pre-charge period (recommended for internal charge pump)
      0xDB, 0x40,                         # VCOMH deselect level
      0x2E,                               # Deactivate scroll
      0xA5,                               # Resume to GDDRAM (use 0xA5 for all-pixels-ON test)
      0xA6,                               # Normal (non-inverted) display
      0xAF                                # Display ON
    ]
    for expected_byte in expected_bytes:
        byte = 0
        for _ in range(8):
            await RisingEdge(scl)
            byte <<= 1
            byte |= bool(sda.value)

        assert byte == expected_byte

        await FallingEdge(scl)
        # Pull SDA low to indicate ACK
        s.i.sda = False

        await FallingEdge(scl)
        # Release SDA
        s.i.sda = True

    # Expect STOP
    await RisingEdge(scl)
    assert not bool(sda.value)

    await RisingEdge(sda)
    assert bool(scl.value)

    # SDA and SCL should remain high
    # This is just to simulate, we could also test it
    for _ in range(100):
        await FallingEdge(clk)
