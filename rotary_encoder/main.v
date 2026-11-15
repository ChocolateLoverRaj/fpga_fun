module main #(
) (
    input rst,
    input clk,
    input rotary_encoder_clk,
    input rotary_encoder_dt,
    input rotary_encoder_sw,
    output [5:0] leds
);
  localparam INITIAL = 1;
  // wire is_clk_low;
  // wire is_dt_low;
  wire is_sw_pressed;

  reg _output = INITIAL;
  reg sw_previously_pressed = 0;
  always @(posedge clk or posedge rst) begin
    if (rst) begin
      _output <= INITIAL;
      sw_previously_pressed <= 0;
    end
    else begin
      if (is_sw_pressed) begin
        if (!sw_previously_pressed) begin
          _output  <= !_output;
          sw_previously_pressed <= 1;
        end
      end
      else begin
        sw_previously_pressed <= 0;
      end
    end
  end

  // assign is_clk_low = ~rotary_encoder_clk;
  // assign is_dt_low = ~rotary_encoder_dt;
  assign is_sw_pressed = ~rotary_encoder_sw;

  // assign leds[0] = ~is_clk_low;
  // assign leds[1] = ~is_dt_low;
  // assign leds[4] = ~is_sw_pressed;
  assign leds[5] = ~_output;

endmodule
