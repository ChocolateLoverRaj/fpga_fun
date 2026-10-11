module _not #(
) (
    input _input,
    output reg _output
);

  assign _output = ~_input;

endmodule


module main #(
) (
    input btn,
    output reg led
);
  wire _output;
  wire _input;


  _not m (_input, _output);

  // The button is active high
  assign _input = btn;
  // The LED is active low
  assign led = ~_output;

endmodule
