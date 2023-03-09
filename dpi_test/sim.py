import os

# verilator --cc --exe --build --sv --timing  hdl/rand_array.sv hdl/adder.v hdl/our.sv sim_main.cpp ../build/libpysv.so

# 创建 DpiConfig对象，传入调用Python函数的SV文件名列表
# cfg = DpiConfig(['our.sv'])

def compile(dut_path, top_file_name, sv_li, v_li, hfn):
    # dut_path = 'hdl/'
    # top_file_name = 'our.sv'
    dut_name = top_file_name.split('.')[0]  # 模块名
    
    # sv_li = ['rand_array.sv']       # 由各python函数生成得到的SV binding文件
    # v_li = ['adder.v', 'our.sv']
    
    v_name = " ".join(sv_li+v_li)
    
    # hfn = 'sim_main.cpp'

    lib_path = 'build/libpysv.so'   # 由各python函数编译得到的共享库
    pysv_lib = "libpysv.so"

    print("\n\n---------------------verilator build info--------------------------\n")

    # 在当前目录创建simulation文件夹
    try:
        os.mkdir("simulation")
    except FileExistsError:
        pass

    # 把所有dut文件和SV binding文件复制到simulation文件夹下
    os.system("cp {}* ./simulation/".format(dut_path))
    
    # 把python函数编译得到的共享库复制到simulation文件夹下
    os.system("cp {} ./simulation/".format(lib_path))

    # 把harness文件复制到simulation文件夹下
    os.system("cp {} ./simulation/".format(hfn))


    # 转换目录到./simulation文件夹下
    os.chdir("./simulation")

    # Using verilator backend
    # --cc                        Create C++ output
    # --trace                     Enable waveform creation
    # --exe                       Link to create executable
    # --prefix <topname>          Name of top level class
    # --top-module <topname>      Name of top level input module
    # --timing                    Enable timing support
    # --build                     Build model executable/library after Verilation
    # -sv                        Enable SystemVerilog parsing
    
    # .so为 与 Verilog 代码链接的可选对象或库文件
    # In the verilator command, include the shared library and the generated binding file
    
    print(
        "verilator --cc --trace --exe --build --sv --timing -top-module {top} {vfn} {hfn} ../{lib}" \
            .format(top=dut_name, vfn=v_name, hfn=hfn, lib=pysv_lib)
            )
    os.system(
        "verilator --cc --trace --exe --build --sv --timing -top-module {top} {vfn} {hfn} ../{lib}" \
            .format(top=dut_name, vfn=v_name, hfn=hfn, lib=pysv_lib))
            
    # # cp libpysv_Top.so ./obj_dir/
    os.system("cp {} ./obj_dir/".format(pysv_lib))

    os.chdir("./obj_dir")    
    os.system(f"./V{dut_name}")


if __name__ == '__main__':
    compile()

