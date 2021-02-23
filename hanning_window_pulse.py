from numpy import cos, sin, linspace, array, zeros, pi, fft
from matplotlib.pyplot import plot, show, xlim, ion, pause, clf, title, xlabel, ylabel, subplot, suptitle
from scipy.signal import hilbert

def Hanning(f, t, n):
	return (1/2)*(1 - cos(f*t/n))*(sin(f*t))

dt = 4e-15
f = 3e8/1550e-9
timesteps = 360
t1 = int(2*pi/(f*dt/5))
src = zeros(timesteps)
for i in range(0, t1):
	src[i] = Hanning(f, i*dt, 5)
subplot(1, 2, 1)
plot(src)
plot(hilbert(src).imag)
plot(abs(hilbert(src)))
title("5 cycle Hann window pulse")
xlabel("Time steps")
ylabel("Amplitude")
xlim(0, t1)
#show()

subplot(1, 2, 2)
spec = fft.fft(src)
freq = fft.fftfreq(spec.size, d=dt)
freq = 2*pi*freq
plot(abs(freq), abs(spec))
title("Frequency response of Hann window")
xlabel("Frequency")
ylabel("Manitude")
xlim(0, 2*f)

suptitle("5 cycle Hann window pulse")
show()
