module _xnor #(
) (
    input input_0,
    input input_1,
    output reg _output
);

  assign _output = ~(input_0 ^ input_1);

endmodule


module main #(
) (
    input [1:0] btns,
    output reg led
);
  wire _output;
  wire input_0;
  wire input_1;


  _xnor m (input_0, input_1, _output);

  // The button is active high
  assign input_0 = btns[0];
  assign input_1 = btns[1];
  // The LED is active low
  assign led = ~_output;

endmodule
