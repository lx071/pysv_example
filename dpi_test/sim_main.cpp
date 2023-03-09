#include "Vour.h"
#include "verilated.h"

#include <memory>
#include <iostream>

using namespace std;

int main(int argc, char** argv)
{
    auto contextp {make_unique<VerilatedContext>()};
    contextp->commandArgs(argc, argv);
    auto top {make_unique<Vour>(contextp.get())};
    
    Verilated::traceEverOn(true);
    
    while(!contextp->gotFinish()){
        top->eval();
        contextp->timeInc(1000);
    }
    return 0;
}