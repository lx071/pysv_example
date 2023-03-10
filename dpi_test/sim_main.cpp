#include "Vour.h"
#include "verilated.h"

#include <memory>
#include <iostream>

using namespace std;

int main(int argc, char** argv)
{
    auto contextp {make_unique<VerilatedContext>()};
    contextp->commandArgs(argc, argv);
<<<<<<< HEAD
    auto top {make_unique<Vour>(contextp.get())};
    
    Verilated::traceEverOn(true);
    
=======
    auto top {make_unique<Vrand_array>(contextp.get())};
    Verilated::traceEverOn(true);
>>>>>>> 209ec876aa954ff039064a6cbbb3634918e90516
    while(!contextp->gotFinish()){
        top->eval();
        contextp->timeInc(1000);
    }
    return 0;
}