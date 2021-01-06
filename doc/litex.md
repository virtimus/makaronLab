

#@refs: https://github.com/litex-hub/fpga_101
#	https://github.com/enjoy-digital/litex/wiki/Installation


#Install Python 3.6+ and FPGA vendor's development tools and/or Verilator.
sudo apt update && sudo apt-get install verilator

#Install Migen/LiteX and the LiteX's cores:(--user to install to user directory)
wget https://raw.githubusercontent.com/enjoy-digital/litex/master/litex_setup.py \
	&& chmod +x litex_setup.py && ./litex_setup.py init install --user ths
export PATH=$PATH:$(echo $PWD/.local/bin/)
 
	
#Later, if you need to update all repositories:
./litex_setup.py update	


#Install a RISC-V toolchain (Only if you want to test/create a SoC with a CPU):
./litex_setup.py gcc
export PATH=$PATH:$(echo $PWD/riscv64-*/bin/)

#install Verilator and test LiteX directly on your computer without any FPGA board:
sudo apt install libevent-dev libjson-c-dev verilator
lxsim --cpu-type=vexriscv


    Run a terminal program on the board's serial port at 115200 8-N-1.

You should get the BIOS prompt like the one below.


#problems 
- paths (fixed)
- g++ command not found -
sudo apt-get install build-essential