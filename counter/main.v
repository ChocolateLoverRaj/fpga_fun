module main
(
    input clk,
    output [5:0] leds
);

localparam [23:0] WAIT_TIME = 24'd13_500_000;
reg [5:0] ledCounter = 0;
reg [23:0] clockCounter = 0;

always @(posedge clk) begin
    clockCounter <= clockCounter + 1;
    if (clockCounter == WAIT_TIME) begin
        clockCounter <= 0;
        ledCounter <= ledCounter + 1;
    end
end

assign leds = ~ledCounter;
endmodule
