import numpy as np

# soft saturate test (from DaisySP)
def soft_saturate(inp, thresh):
    flip = inp < 0.0
    val = -inp if flip else inp
    out = 0.0
    
    if val < thresh:
        out = inp
    elif val > 1.0:
        out = (thresh + 1.0) / 2.0
        if flip:
            out *= -1.0
    elif val > thresh:
        temp = (val - thresh) / (1 - thresh)
        out = thresh + (val - thresh) / (1.0 + (temp * temp))
        if flip:
            out *= -1.0
    
    return out

# soft limit (From DaisySP)
def SoftLimit(x):
    return x * (27 + x * x) / (27 + 9 * x * x)

# soft clip (from DaisySP)
def SoftClip(x):
    if x < -3.0:
        return -1.0
    elif x > 3.0:
        return 1.0
    else:
        return SoftLimit(x)
    
def SLOPE(output, inpint, positive, negative):
  error = (inpint) - output
  output += (positive if error > 0 else negative) * error

def Limiter(pre_gain,input):
    peak_ = 0.5
    s = input * pre_gain
    SLOPE(peak_, np.abs(s), 0.05, 0.00002)
    gain = 1.0 if peak_ <= 1.0 else 1.0 / peak_
    input += s * gain * 0.8
    return input
