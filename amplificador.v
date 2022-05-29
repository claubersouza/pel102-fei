// File: amplificador.v
// Generated by MyHDL 0.11
// Date: Sat May 21 12:00:46 2022


`timescale 1ns/10ps

module amplificador (
    clk,
    seno,
    ganho,
    saida
);


input [1:0] clk;
input [7:0] seno;
input [3:0] ganho;
output [7:0] saida;
reg [7:0] saida;


always @(*) begin: AMPLIFICADOR_LOGIC
    saida <= seno * ganho;
end

endmodule
