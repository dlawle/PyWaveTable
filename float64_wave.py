import numpy as np
import matplotlib.pyplot as plt
import wave
import dsp

def equation(x, s, frequency=440):
    n_values = np.arange(s, 101)
    angular_frequency = 2 * np.pi * frequency
    result =  np.sin(x)-(1/2)*np.sin(2*x)+(1/3)*np.sin(3*x)-(1/4)*np.sin(4*x)+(1/5)*np.sin(5*x)-(1/6)*np.sin(6*x)
    return result

# Number of samples
num_samples = 4000

# Range of 's' values (start and end)
s_start = 5
s_end = 100

# Create an array of 'x' values
x_values = np.linspace(0, 25, num_samples)

# Set the initial frequency (440 Hz)
initial_frequency = 440

# Calculate the equation for each 'x' value using the initial frequency
result_values = np.zeros(num_samples)
for i in range(num_samples):
    result_values[i] = equation(x_values[i], s_start, frequency=initial_frequency)

# Apply  soft_saturate 
soft_saturate_vectorized = np.vectorize(dsp.soft_saturate)
processed_values_soft_saturate = soft_saturate_vectorized(result_values, 0.0)

# Apply Limiter
limiter_vectorized = np.vectorize(dsp.Limiter)
processed_limitor = limiter_vectorized(0.5, result_values)

# Apply soft_clip
soft_clip_vectorized = np.vectorize(dsp.SoftClip)
processed_values_soft_clip = soft_clip_vectorized(result_values)

# Save the wavetable to a WAV file
filename = "generators/output/wavetable.wav"
with wave.open(filename, 'w') as wf:
    wf.setnchannels(1)          # Mono channel
    wf.setsampwidth(2)          # 2 bytes per sample (int16)
    wf.setframerate(44100)      # 44.1 kHz sample rate
    wf.writeframes((x_values * 32767).astype(np.int16).tobytes())

def wrtieWave():
    # Save the wavetable to a WAV file
    filename = "generators/output/wavetable.wav"
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)          # Mono channel
        wf.setsampwidth(2)          # 2 bytes per sample (int16)
        wf.setframerate(44100)      # 44.1 kHz sample rate
        wf.writeframes((processed_values_soft_saturate * 32767).astype(np.int16).tobytes())

# Plot the result
plt.plot(x_values, result_values, label='Original')
#plt.plot(x_values, processed_values_soft_saturate, label='Soft Saturation')
#plt.plot(x_values, processed_values_soft_clip, label='Soft Clip')
#plt.plot(x_values, processed_limitor, label="Limitor")

plt.xlabel('x')
plt.ylabel('y')
plt.title('Equation: y = Σ(sin(2nx) / (2n) * cos(2πf))')
plt.grid(True)
plt.legend()
plt.show()
#wrtieWave()
