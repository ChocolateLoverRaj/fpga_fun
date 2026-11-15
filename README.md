# FPGA Projects
Exploring FPGAs.

This is my first time playing with FPGAs. Before this my only experience was completing [nandgame](https://nandgame.com/).

## Hardware
I bought [this Tang Nano 20K from AliExpress](https://www.aliexpress.us/item/3256805394833478.html) (the "Nano 20K No header" variant). It costed around $30. For now all of these projects should work with all Tang Nanos (1K, 4K, 9K, 20K). Currently only 20K is supported, but it will be really easy to support the others.

## Running the examples
There is a Rust project at the top level directory. Run
```bash
cargo run
```
to see the commands. For example, to run the counter program:
```bash
cargo r -- --board tangnano20k --project counter run
```

## Directory structure
Each project has its own directory, with the following files:
`main.v`: The core logic.
`<board name>.cst`: The constraints file for the board for that project.
`test.v`: The simulation for [iverilog](https://github.com/steveicarus/iverilog) (optional).

## References
- https://learn.lushaylabs.com/tang-nano-series/
