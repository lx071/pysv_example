import os
import subprocess

# dpi
class DpiConfig(object):
    def __init__(self, pysv_li, pkg_sv_path=".sv/pkg/pysv_pkg.sv", lib_path=".build/libpysv.so"):
        self.sv = pkg_sv_path
        self.lib = lib_path
        self.bname = " ".join(pysv_li)
        ...
# verilator --cc --exe --build --sv --timing  hdl/rand_array.sv hdl/adder.v hdl/our.sv sim_main.cpp ../build/libpysv.so

# 创建 DpiConfig对象，传入调用Python函数的SV文件名列表
# cfg = DpiConfig(['our.sv'])

def compile():
    dut_path = 'hdl/'
    top_module_name = 'our.sv'
    dut_name = top_module_name.split('.')[0]  # 模块名
    # sv = '.sv/pkg/pysv_pkg.sv'
    lib_path = 'build/libpysv.so'
    
    sv_li = ['rand_array.sv']
    v_li = ['adder.v', 'our.sv']
    v_name = " ".join(v_li)

    print("\n\n---------------------verilator build info--------------------------\n")

    # 在当前目录创建simulation文件夹
    try:
        os.mkdir("simulation")
    except FileExistsError:
        pass

    # 把所有dut文件复制到simulation文件夹下
    os.system("cp {}* ./simulation/".format(dut_path))

    # vfn = "{}.v".format(self.dut_name)              # {dut_name}.v
    vfn = top_module_name
    hfn = "{}-harness.cpp".format(dut_name)    # {dut_name}-harness.cpp
    mfn = "V{}.mk".format(dut_name)            # V{dut_name}.mk
    efn = "V{}".format(dut_name)               # V{dut_name}
    bname = ''
    cpp_path = 'sim_main.cpp'
    # " ".join(pysv_li)

    # dpiconfig对象
    # self.sv = pkg_sv_path     # .sv/pkg/pysv_pkg.sv
    # self.lib = lib_path       # .build/libpysv.so
    # self.bname = " ".join(pysv_li)  # pysv_li存放调用了python函数的SV列表 (Add.sv)
    pysv_pkg = "{}_pysv_pkg.sv".format(dut_name)       # {dut_name}_pysv_pkg.sv
    pysv_lib = "libpysv.so"
    # cp .sv/pkg/pysv_pkg.sv ./simulation/{dut_name}_pysv_pkg.sv        # 由各python函数生成得到的SV binding文件
    # os.system("cp {} ./simulation/{}_pysv_pkg.sv".format(sv, dut_name))
    
    # cp .build/libpysv.so ./simulation/libpysv_{dut_name}.so           # 由各python函数编译得到的共享库
    os.system("cp {} ./simulation/".format(lib_path))

    os.system("cp {} ./simulation/".format(cpp_path))


    # 转换目录到./simulation文件夹下
    os.chdir("./simulation")

    # Using verilator backend
    # --cc                        Create C++ output
    # --trace                     Enable waveform creation
    # --exe                       Link to create executable
    # --prefix <topname>          Name of top level class
    # --top-module <topname>      Name of top level input module
    # .so为 与 Verilog 代码链接的可选对象或库文件
    # In the verilator command, include the shared library and the generated binding file
    # verilator --cc --trace --exe --prefix VTop --top-module Top Top_pysv_pkg.sv {bbx} libpysv_Top.so Top-harness.cpp
    # verilator --cc --trace --exe --prefix VTop --top-module Top Top_pysv_pkg.sv Add.sv Top.v libpysv_Top.so Top-harness.cpp

    # verilator --cc --exe --build --sv --timing  hdl/rand_array.sv hdl/adder.v hdl/our.sv sim_main.cpp ../build/libpysv.so
    
    # print(
    #     "verilator --cc --trace --exe --prefix {prefix} --top-module {top} {pkg} {bbx} {vfn} {lib} {hfn}" \
    #         .format(top=dut_name, bbx=bname, vfn=vfn, hfn=hfn, pkg=pysv_pkg, lib=pysv_lib,
    #                 prefix=efn))
    # os.system(
    #     "verilator --cc --trace --exe --prefix {prefix} --top-module {top} {pkg} {bbx} {vfn} {lib} {hfn}" \
    #         .format(top=dut_name, bbx=bname, vfn=vfn, hfn=hfn, pkg=pysv_pkg, lib=pysv_lib,
    #                 prefix=efn))
    
    # "verilator --cc --exe --build --sv --timing  rand_array.sv adder.v our.sv sim_main.cpp libpysv.so"
    # verilator --cc --exe --prefix Vour -build --sv --timing  --top-module our rand_array.sv adder.v our.sv libpysv.so sim_main.cpp 
    print(
        "verilator --cc --exe --build --sv --timing  rand_array.sv adder.v our.sv sim_main.cpp ../libpysv.so"
        )
    os.system(
        "verilator --cc --trace --exe --build --sv --timing rand_array.sv adder.v our.sv sim_main.cpp ../libpysv.so"
            )
    # # cp libpysv_Top.so ./obj_dir/
    os.system("cp {} ./obj_dir/".format(pysv_lib))
    # ./obj_dir/V{dut_name}
    # os.system("pwd")

    # 确保 libpysv.so（共享库） 在 LD_LIBRARY_PATH 中--  pysv要求的
    # env = {"LD_LIBRARY_PATH": "."}          # 环境变量
    # args = [f"./obj_dir/Vrand_array"]        # ./obj_dir/V{dut_name}

    # # 创建子进程执行./obj_dir/{dut_name}
    # subprocess.Popen(args, env=env)
    os.chdir("./obj_dir")    
    os.system("./Vrand_array")


if __name__ == '__main__':
    compile()

