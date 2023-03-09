import os

# dpi
class DpiConfig(object):
    def __init__(self, pysv_li, pkg_sv_path=".sv/pkg/pysv_pkg.sv", lib_path=".build/libpysv.so"):
        self.sv = pkg_sv_path
        self.lib = lib_path
        self.bname = " ".join(pysv_li)
        ...

# 创建 DpiConfig对象，传入调用Python函数的SV文件名列表
cfg = DpiConfig(['our.sv'])

def compile():
    dut_path = 'hdl/'
    top_module_name = 'our.sv'
    dut_name = top_module_name.split('.')[0]  # 模块名
    # sv = '.sv/pkg/pysv_pkg.sv'
    lib = '.build/libpysv.so'
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
    # " ".join(pysv_li)

    # dpiconfig对象
    # self.sv = pkg_sv_path     # .sv/pkg/pysv_pkg.sv
    # self.lib = lib_path       # .build/libpysv.so
    # self.bname = " ".join(pysv_li)  # pysv_li存放调用了python函数的SV列表 (Add.sv)
    pysv_pkg = "{}_pysv_pkg.sv".format(dut_name)       # {dut_name}_pysv_pkg.sv
    pysv_lib = "libpysv_{}.so".format(dut_name)        # libpysv_{dut_name}.so

    # cp .sv/pkg/pysv_pkg.sv ./simulation/{dut_name}_pysv_pkg.sv        # 由各python函数生成得到的SV binding文件
    # os.system("cp {} ./simulation/{}_pysv_pkg.sv".format(sv, dut_name))
    
    # cp .build/libpysv.so ./simulation/libpysv_{dut_name}.so           # 由各python函数编译得到的共享库
    os.system("cp {} ./simulation/libpysv_{}.so".format(lib, dut_name))

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
    print(
        "verilator --cc --trace --exe --prefix {prefix} --top-module {top} {pkg} {bbx} {vfn} {lib} {hfn}" \
            .format(top=dut_name, bbx=bname, vfn=vfn, hfn=hfn, pkg=pysv_pkg, lib=pysv_lib,
                    prefix=efn))
    os.system(
        "verilator --cc --trace --exe --prefix {prefix} --top-module {top} {pkg} {bbx} {vfn} {lib} {hfn}" \
            .format(top=dut_name, bbx=bname, vfn=vfn, hfn=hfn, pkg=pysv_pkg, lib=pysv_lib,
                    prefix=efn))
    # cp libpysv_Top.so ./obj_dir/
    os.system("cp {} ./obj_dir/".format(pysv_lib))
    # ./obj_dir/V{dut_name}
    os.system("./obj_dir/V{}")