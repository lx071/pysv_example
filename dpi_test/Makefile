#####################################################################
  
# make all

all: compile

first:
	date +%M.%s.%N

second:
	date +%M.%s.%N

end:
	date +%M.%s.%N

# only make compile

compile:
	python test_adder.py

# only make visual ( make .elf file to the .vcd file )

run:
	verilator --cc --exe --build --sv --timing hdl/rand_array.sv hdl/adder.v hdl/our.sv sim_main.cpp ../build/libpysv.so
        # verilator --cc --exe --build --sv --timing --trace hdl/rand_array.sv hdl/adder.v hdl/our.sv sim_main.cpp ../build/libpysv.so

# only open the wave

sim:
	gtkwave simulation/obj_dir/dump.vcd

# clear middle files

clean:
	rm -rf build simulation __pycache__