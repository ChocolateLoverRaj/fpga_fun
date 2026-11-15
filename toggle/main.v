module toggle #(
  parameter INITIAL_OUTPUT = 1'b0
) (
  input wire clk,
  input wire rst,
  input wire _input,
  output reg  _output = INITIAL_OUTPUT
);

  reg prev_input = 1'b0;

  always @(posedge clk or posedge rst) begin
    if (rst) begin
      _output <= INITIAL_OUTPUT;
      prev_input <= 1'b0;
    end else begin
      if (_input && !prev_input) begin
        _output <= ~_output;
      end
      prev_input <= _input;
    end
  end

endmodule

module main #(
) (
    input clk,
    input rst,
    input btn,
    output led
);
  wire _output;
  toggle #(.INITIAL_OUTPUT(1)) toggle_inst (.clk(clk), .rst(rst), ._input(btn), ._output(_output) );
  // The LED is active low
  assign led = ~_output;

endmodule
