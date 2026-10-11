module half_adder #(
) (
    input input_0,
    input input_1,
    output wire sum,
    output wire carry_out
);

  assign sum = input_0 ^ input_1;
  assign carry_out = input_0 & input_1;

endmodule


module main #(
) (
    input [1:0] btns,
    output [1:0] leds
);
  wire input_0;
  wire input_1;
  wire sum;
  wire carry_out;


  half_adder m (input_0, input_1, sum, carry_out);

  // The button is active high
  assign input_0 = btns[0];
  assign input_1 = btns[1];
  // The LED is active low
  assign leds[0] = ~sum;
  assign leds[1] = ~carry_out;

endmodule
