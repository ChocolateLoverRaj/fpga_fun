build_dir := "build"
board := "tangnano20k"

run project:
    mkdir -p {{build_dir}}/{{project}}
    yosys -p "read_verilog {{project}}/main.v; synth_gowin -top main -json {{build_dir}}/{{project}}/main.json"
    nextpnr-himbaechel --json {{build_dir}}/{{project}}/main.json --freq 27 --write {{build_dir}}/{{project}}/main_pnr.json --device GW2AR-LV18QN88C8/I7 --vopt family=GW2A-18C --vopt cst={{project}}/{{board}}.cst
    gowin_pack -d GW2A-18C -o {{build_dir}}/{{project}}/main.fs {{build_dir}}/{{project}}/main_pnr.json
    openFPGALoader -b {{board}} {{build_dir}}/{{project}}/main.fs
