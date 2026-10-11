use std::{
    fs::create_dir_all,
    io::{self},
    path::PathBuf,
    process::Command,
};

use clap::{Parser, Subcommand, ValueEnum};

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum Board {
    Tangnano20k,
}

struct BoardInfo {
    next_pnr_device: &'static str,
    next_pnr_family: &'static str,
    gowin_pack_device: &'static str,
    open_fpga_loader_board: &'static str,
}

impl Board {
    pub fn info(&self) -> BoardInfo {
        BoardInfo {
            next_pnr_device: "GW2AR-LV18QN88C8/I7",
            next_pnr_family: "GW2A-18C",
            gowin_pack_device: "GW2A-18C",
            open_fpga_loader_board: "tangnano20k",
        }
    }
}

#[derive(Parser)]
#[command(version, about)]
struct Cli {
    #[arg(long, default_value = "build")]
    build_dir: PathBuf,

    #[arg(long)]
    board: Board,

    #[arg(long)]
    project: String,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Build,
    Run,
    Simulate,
}

fn main() -> color_eyre::Result<()> {
    color_eyre::install()?;
    let Cli {
        board,
        build_dir,
        project,
        command,
    } = Cli::parse();

    let build_dir_str = build_dir.to_str().unwrap();
    let BoardInfo {
        next_pnr_device,
        next_pnr_family,
        gowin_pack_device,
        open_fpga_loader_board,
    } = board.info();
    let create_output_dir = || create_dir_all(build_dir.join(&project));
    let build = || -> color_eyre::Result<()> {
        create_output_dir()?;
        run_command(
            Command::new("yosys").arg("-p").arg(
                [
                    format!("read_verilog {project}/main.v"),
                    format!("synth_gowin -top main -json {build_dir_str}/{project}/main.json"),
                ]
                .join("; "),
            ),
        )?;
        run_command(
            Command::new("nextpnr-himbaechel")
                .arg("--json")
                .arg(format!("{build_dir_str}/{project}/main.json"))
                .arg("--freq")
                .arg("27")
                .arg("--write")
                .arg(format!("{build_dir_str}/{project}/pnr.json"))
                .arg("--device")
                .arg(next_pnr_device)
                .arg("--vopt")
                .arg(format!("family={next_pnr_family}"))
                .arg("--vopt")
                .arg(format!("cst={project}/{open_fpga_loader_board}.cst")),
        )?;
        run_command(
            Command::new("gowin_pack")
                .arg("--device")
                .arg(gowin_pack_device)
                .arg("--output")
                .arg(format!("{build_dir_str}/{project}/main.fs"))
                .arg(format!("{build_dir_str}/{project}/pnr.json")),
        )?;
        Ok(())
    };

    match command {
        Commands::Build => {
            build()?;
        }
        Commands::Simulate => {
            create_output_dir()?;
            let output_file = format!("{build_dir_str}/{project}/test.o");
            run_command(
                Command::new("iverilog")
                    .arg("-o")
                    .arg(&output_file)
                    .arg("-s")
                    .arg("test")
                    .arg(format!("{project}/main.v"))
                    .arg(format!("{project}/test.v")),
            )?;
            run_command(Command::new("vvp").arg(output_file))?;
        }
        Commands::Run => {
            build()?;
            run_command(
                Command::new("openFPGALoader")
                    .arg("--board")
                    .arg(open_fpga_loader_board)
                    .arg(format!("{build_dir_str}/{project}/main.fs")),
            )?;
        }
    }

    Ok(())
}

fn run_command(command: &mut Command) -> Result<(), io::Error> {
    let exit_status = command.spawn()?.wait()?;
    if !exit_status.success() {
        Err(io::Error::other(format!(
            "command failed with status {exit_status}"
        )))?;
    }
    Ok(())
}
