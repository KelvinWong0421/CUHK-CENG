set init_verilog cla4_synth.v
set init_top_cell cla4
set init_lef_file FreePDK45/gscl45nm.lef
set init_pwr_net vdd
set init_gnd_net gnd
set init_mmmc_file mmmc.tcl
init_design
floorPlan -r 1 0.96 4.0 4.0 4.0 4.0
globalNetConnect vdd -type pgpin -pin vdd -inst *
globalNetConnect gnd -type pgpin -pin gnd -inst *
sroute -nets {vdd gnd}
addRing -center 1 -spacing 0.5 -width 0.5 -layer {top 3 bottom 3 left 4 right 4} -nets { gnd vdd }
addStripe -nets {vdd gnd} -layer 4 -direction vertical -width 0.4 -spacing 0.5 -set_to_set_distance 5 -start 0.5
addStripe -nets {vdd gnd} -layer 3 -direction horizontal -width 0.4 -spacing 0.5 -set_to_set_distance 5 -start 0.5
place_design
addFiller -cell FILL -prefix FILL -fillBoundary
assignIoPins
routeDesign
verify_drc
report_area
report_power
report_timing
puts "The die area is [get_db designs .area] square micron"