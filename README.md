```
yosys -p "read_verilog counter.v; synth_gowin -top counter -json counter.json"
nextpnr-himbaechel --json counter.json --freq 27 --write counter_pnr.json --device GW2AR-LV18QN88C8/I7 --vopt family=GW2A-18C --vopt cst=counter.cst
gowin_pack -d GW2A-18C -o counter.fs counter_pnr.json
openFPGALoader -b tangnano20k counter.fs
```