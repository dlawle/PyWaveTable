import numpy as np
import wave
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Function to generate the wavetable
num_samples = 44100

def generate_custom_wavetable(t, num_samples, frequency=440.0): 
    num_cycles = int(frequency * num_samples / 44100) # note - 44100 here = sample rate 
    n_values = np.arange(num_samples)
    wavetable = np.sin((2 * np.pi / num_samples) * t * n_values * num_cycles)
    wavetable /= np.max(np.abs(wavetable))
    return wavetable

def generate_fourier_wavetable(num_samples, frequency=440.0):
    num_cycles = int(frequency * num_samples / 44100) # note - 44100 here = sample rate 
    n_values = np.arange(num_samples)
    


# Initialize the figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
plt.xlim([0,100])


# Initial value for t
initial_t = 5.0

# Generate the initial wavetable
wavetable = generate_custom_wavetable(initial_t, num_samples)

line, = ax.plot(wavetable)
ax.set_title(f"Wavetable with t = {initial_t}, Num Samples = {num_samples}")
ax.set_xlabel("Sample Index")
ax.set_ylabel("Value")
ax.grid()

# Create the slider for t
axcolor = "lightgoldenrodyellow"
ax_t = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
s_t = Slider(ax_t, "t", 1.0, 20.0, valinit=initial_t)

# Function to update the plot, audio, and save the WAV file
def update(val):
    t = s_t.val
    wavetable = generate_custom_wavetable(t, num_samples)
    line.set_ydata(wavetable)
    ax.set_title(f"Wavetable with t = {t}, Num Samples = 64")
    fig.canvas.draw_idle()

    # Save the wavetable to a WAV file
    filename = "generators/output/wavetable.wav"
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)          
        wf.setsampwidth(2)          
        wf.setframerate(44100)      
        wf.writeframes((wavetable * 32767).astype(np.int16).tobytes())

s_t.on_changed(update)

def write_wavetable_to_file(wavetable, filename):
    with open(filename, "w") as file:
        count = 0
        for sample in wavetable:
            file.write(f"{sample:.6f},\t")
            count += 1
            if count == 6:
                file.write("\n")
                count = 0
        # Remove the trailing comma from the last line
        file.seek(file.tell() - 1)
        file.truncate()



def create_window():
    plt.show()

if __name__ == "__main__":
    write_wavetable_to_file(wavetable, "generators/output/wavetable.tbl")
    plt.show()
