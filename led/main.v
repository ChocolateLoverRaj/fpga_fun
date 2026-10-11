module main #(
) (
    input btn,
    output reg led
);
  wire _input;
  wire _output;

  assign _output = _input;

  // The button is active high
  assign _input = btn;
  // The LED is active low
  assign led = ~_output;

endmodule
