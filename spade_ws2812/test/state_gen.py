# top = state_gen_th

from cocotb.triggers import FallingEdge

import cocotb
from spade import SpadeExt
from cocotb.clock import Clock

async def check_led(clk, s, index):
    # Each bit of the LED should be emitted
    for b in range(0, 24):
        # And each duration from 0 to us1_25 in each bit
        # For simulation performance, we'll just check the first and last bit explicitly
        await FallingEdge(clk)
        s.o.assert_eq(f"OutputControl::Led {{ payload: {index}, bit: {b}, duration: 0 }}")
        for d in range(0, 5):
            await FallingEdge(clk)
        s.o.assert_eq(f"OutputControl::Led {{ payload: {index}, bit: {b}, duration: 5 }}")

@cocotb.test()
async def normal_operation(dut):
    s = SpadeExt(dut)

    clk = dut.clk_i
    await cocotb.start(Clock(clk, 1, units='ns').start())

    s.i.rst = "true"
    await FallingEdge(clk)
    s.i.rst = "false"

    s.o.assert_eq("OutputControl::Ret()")

    s.i.timing = """Timing {
        us280: 28,
        us0_4: 4,
        us0_8: 8,
        us0_45: 4,
        us0_85: 8,
        us1_25: 12,
    }"""

    for i in range(0, 28):
        await FallingEdge(clk)
        s.o.assert_eq("OutputControl::Ret()")

    # Check all 10 leds
    for i in range(0, 10):
        await check_led(clk, s, i)

    # Ensure we get back to the ret state
    await FallingEdge(clk)
    s.o.assert_eq("OutputControl::Ret()")
