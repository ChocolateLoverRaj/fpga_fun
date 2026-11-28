# top = ssd1306_th

from typing import TypedDict

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ReadOnly, RisingEdge
from spade import SpadeExt


async def settle():
    """
    Wait for the current cycle to propagate, can sample outputs after this
    """

    await ReadOnly()


async def advance(dut):
    """
    Cross the clock edge. Drive DUT inputs after this returns.
    """

    await RisingEdge(dut.clk)


async def step(dut):
    """
    Settle then advance, without sampling in between.
    """

    await settle()
    await advance(dut)

class Config(TypedDict):
    start_hold_cycles: int
    data_hold_cycles: int
    data_setup_cycles: int
    scl_low_cycles: int
    scl_high_cycles: int
    scl_cycles: int
    stop_setup_cycles: int
    after_stop_cycles: int
    restart_setup_cycles: int

    data_valid_ack_time: int

config_400_khz: Config = {
    "start_hold_cycles": 6,
    "data_hold_cycles": 3,
    "data_setup_cycles": 1,
    "scl_low_cycles": 13,
    "scl_high_cycles": 6,
    "scl_cycles": 25,
    "stop_setup_cycles": 6,
    "after_stop_cycles": 13,
    "restart_setup_cycles": 6,
    "data_valid_ack_time": 9,
}

async def reset(dut):
    s = SpadeExt(dut)
    s.i.rst = True
    await step(dut)
    s.i.rst = False

async def setup(config: Config, dut):
    s = SpadeExt(dut)
    clk = dut.clk

    # 1. Start 10 MHz clock (100 ns period)
    cocotb.start_soon(Clock(clk, 100, unit="ns").start())

    s.i.rst = False
    s.i.sda = True
    s.i.scl = True
    s.i.config.start_hold_cycles = config["start_hold_cycles"]
    s.i.config.data_hold_cycles = config["data_hold_cycles"]
    s.i.config.data_setup_cycles = config["data_setup_cycles"]
    s.i.config.scl_low_cycles = config["scl_low_cycles"]
    s.i.config.scl_high_cycles = config["scl_high_cycles"]
    s.i.config.scl_cycles = config["scl_cycles"]
    s.i.config.stop_setup_cycles = config["stop_setup_cycles"]
    s.i.config.after_stop_cycles = config["after_stop_cycles"]
    s.i.config.restart_setup_cycles = config["restart_setup_cycles"]

    await reset(dut)

@cocotb.test()
async def simple_test(dut):
    await setup(config_400_khz, dut)
    s = SpadeExt(dut)
    clk = dut.clk
    # sda = dut.sda
    # scl = dut.scl

    s.i.sda = False

    for _ in range(6564):
        await RisingEdge(clk)

#     while s.o.sda == True:
#         await step(dut)
#     while s.o.scl == True:
#         await step(dut)
#
#     byte = 0
#     for _ in range(8):
#         while s.o.scl == False:
#             await step(dut)
#         byte <<= 1
#         byte |= bool(s.o.sda)
#
#     addr = byte >> 1
#     read_write = bool(byte & (1 << 7))
#
#     assert addr == 0x3C
#     assert read_write == 0
#
#     while s.o.scl == True:
#         await step(dut)
#     # Pull SDA low to indicate ACK
#     s.i.sda = False
#
#     while s.o.scl == False:
#         await step(dut)
#     while s.o.scl == True:
#         await step(dut)
#     # Release SDA
#     s.i.sda = True
#
#     # Receive data
#     expected_bytes = [
#       0x00,                               # Control byte: command stream
#       0xAE,                               # Display OFF
#       0xD5, 0x80,                         # Clock divide / oscillator frequency
#       0xA8, 0x3F,                         # Multiplex ratio (64 rows for 128x64)
#       0xD3, 0x00,                         # Display offset (0)
#       0x40,                               # Display start line (0)
#       0x8D, 0x14,                         # Enable internal charge pump (crucial for SSD1306!)
#       0x20, 0x00,                         # Horizontal addressing mode
#       0xA1,                               # Segment re-map (col 127 -> SEG0)
#       0xC8,                               # COM scan direction (remapped)
#       0xDA, 0x12,                         # COM pins hardware config (0x12 for 128x64; 0x02 for 128x32)
#       0x81, 0xCF,                         # Contrast control
#       0xD9, 0xF1,                         # Pre-charge period (recommended for internal charge pump)
#       0xDB, 0x40,                         # VCOMH deselect level
#       0x2E,                               # Deactivate scroll
#       0xA5,                               # Resume to GDDRAM (use 0xA5 for all-pixels-ON test)
#       0xA6,                               # Normal (non-inverted) display
#       0xAF                                # Display ON
#     ]
#     for expected_byte in expected_bytes:
#         byte = 0
#         for _ in range(8):
#             while s.o.scl == False:
#                 await step(dut)
#             byte <<= 1
#             byte |= bool(sda.value)
#
#         assert byte == expected_byte
#
#         await FallingEdge(scl)
#         # Pull SDA low to indicate ACK
#         s.i.sda = False
#
#         await FallingEdge(scl)
#         # Release SDA
#         s.i.sda = True
#
#     # Expect STOP
#     await RisingEdge(scl)
#     assert not bool(sda.value)
#
#     await RisingEdge(sda)
#     assert bool(scl.value)
#
#     # SDA and SCL should remain high
#     # This is just to simulate, we could also test it
#     for _ in range(100):
#         await FallingEdge(clk)
