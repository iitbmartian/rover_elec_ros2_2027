# Shoulder (1) / elbow (2) BLDC command, in JOINT units (radians, rad/s).
# odrive_can converts to ODrive motor turns using the gear ratios.
#
# pos_vel = true  -> position control: pos1/pos2 are the targets, vel1/vel2 are velocity feed-forward
# pos_vel = false -> velocity control: vel1/vel2 are the commanded joint velocities (pos1/pos2 are
#                    informational only, e.g. for joint_state_bridge / RViz)
bool pos_vel
float32 pos1
float32 pos2
float32 vel1
float32 vel2
