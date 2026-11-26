# plan
# first send it a low constant pwm command until it hits a limit switch (call this LS 1) and take reading
# then make it go in the opposite direction at some low constant pwm and constantly read encoder values say every t s
# wait until it hits the other limit switch (LS 2) and see how long this took say T s
# so then angular speed (ideally constant) was 330/T dps = w
# so the nth reading (upto an offset) was at time nt + k seconds after the rotation started
# angle wouldve been theta = w(nt + k) from limit switch 1
# from every reading subtract appropriate amount to make LS 1 the zero point and deal with wraparound wherever it happens- i'll call these readings xn
# now w(nt+k) = a0 sin(xn) + a1 cos(xn) + b0 sin(2xn) + b1 cos(2xn) type shit where im measuring everything in appropriate angular units to make this work 
# (so xn will vary from 0 to 2pi and w(nt+k) needs to be in radians too)
# now do a best fit to find all the missing constants so take more than enough readings for this- I'd like 20 readings at least over the 330 degrees I think 

# how to -> compare against quadrature to improve accuracy?
# -> figure out if they actually do the 330 degrees
# -> how to measure time accurately
# -> do all processing afterwards to make stuff vaguely synchronous warna probably fuck ho jayega
# -> can we use some sort of pakka working source of data instead of just hoping it does constant velocity- idts
# -> can definitely improve by increasing the number of parameters to account for more unknowns and just taking more readings correspondingly


# 