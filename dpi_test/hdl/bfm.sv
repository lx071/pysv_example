import rand_array::*;

`timescale 1ns/1ps
module our ();

parameter int LENGTH = 1000000;

bit clk_i, reset_i;
int index = 0; // 当前索引

always #1 clk_i = ~clk_i;

bit [7:0] a_arr[LENGTH], b_arr[LENGTH];

initial begin
    string s = get_rand_array(LENGTH*2);
    int i = 0;
    int j = 0;
    int k = 0;
    while(s[i]!=0)begin
        if(s[i] == 8'h7d) begin
            i = i +1;
            a_arr[j] = s[i]^8'h20;
        end else begin
            a_arr[j] = s[i];
        end
        i = i +1;
        if(s[i] == 8'h7d) begin
            i = i +1;
            b_arr[k] = s[i]^8'h20;
        end else begin
            b_arr[k] = s[i];
        end
        i = i+1;
        j = j+1;
        k = k+1;
    end
    clk_i = 0;
    reset_i = 1;
end

reg [7:0] a, b;
wire [7:0] res;

always @(posedge clk_i)
begin
    if(!reset_i) begin
        a <= 8'b0;
        b <= 8'b0;
        
    end
    else if(index < LENGTH) begin
        a <= a_arr[index];
        b <= b_arr[index];
        index <= index + 1;
    end else if(index == LENGTH) begin
        $finish;
    end
end

adder adder_inst(
    .clk_i(clk_i),
    .reset_i(reset_i),
    .a(a),
    .b(b),
    .res(res)
);

initial begin
    $dumpfile("dump.vcd");
    $dumpvars;
end

endmodule