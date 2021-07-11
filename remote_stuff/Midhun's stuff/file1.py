import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert


#Surface Design
#Initate the grid
nx =1330 
nz =2500 
# nx =140
# nz =2500 
irx=[]
irz=[]
dx=0.1
dz=0.1
xn=dx*nx
zn=dz*nz
#Plot the axis
f2 = plt.figure(figsize=(8, 4));
fig1 =  f2.add_subplot(1, 1, 1 );
#plt.axis([-xn,xn,0,zn])
plt.axis([-xn,xn,0,50])

#plt.text(0,40,'o')  #Plot the source 
#plt.text(0,80,'o')
#Plot the recivers
theta = np.linspace(np.pi/18, 17*np.pi/18, 20)
#r=0.70  # Radius


#for i in theta:
 #   x=r*np.cos(i)
  #  z=r*np.sin(i)
# Receiver locations
  #  irx = np.append(irx,x)
  #  irz = np.append(irz,z)
  #  plt.text(x,z,'+')

#Initialize the velocity model
c0=33000 #Velocity of the fixed media
c = np.zeros((nz,2*nx))
c += c0
c[-53:200,:] =0.8*c0
#c[-20:196,:] = c0#Deafault for two mediums=0.8
for i in range(38):
    c[-230:-5,i*70+40:(i+1)*70]=c0
    c[-230:-5,i*70+15:(i*70)+27]=c0
    c[-44:-5,i*70+15:i*70+27]=0
    c[-230:-5,i*70:i*70+15]=0
    c[-230:-5,i*70+27:i*70+41]=0
    c[-230:-5,-30:]=0
    
    #c[-53:-5,i*13+10]=0
    #c[-53:-5,i*13]=0
    #c[-9,:]=0
    #c[-5,i*13+1:i*13+10]=0
    #c[-9:-5,i*13+10:i*13+14]=0
    #c[-4:200,:]=0.4*c0
for j in range(19):
    c[-82+4*j:-3,j*70+40:j*70+71]=0
    c[-82+4*j:-3,-(70*j+30):-(0+70*j)]=0
    
#c[0,:]=c0
#c[-53:,0:200]=0
#c[-53:,-199:]=0
plt.imshow(c,extent =[-xn, xn,0, zn])
plt.colorbar()
#plt.show()
plt.savefig("file1_1.png")


wav=79
f0 = c0/wav    # dominant frequency of source 
ist =100    # shifting of source time function 
T = 1.0 / f0  # dominant period
nt = 250000   # number of time steps. Assumed 60 to avoid extra reflected waves
dt = 0.000001   # Time step default =0.001
dx = 0.1# default=1,grid increment in x - 1
#wav=c0/f0 # Wavelength of the wave

k0=2*np.pi/wav #Free-space phase constant
seis = np.zeros((len(irx), nt))
# Source time function 
src = np.zeros(nt)   #nt+1 for gaussian
t1=int(1*2*np.pi/(f0*dt/1)) # Time period of a single pulse, change value if using different cycle pulse
for it in range(t1+1):
    src[it]= 1/2*(1-(np.cos(f0*(it)*dt/1)))*(np.sin(f0*(it)*dt))#dt/3 for 3 cycle pulse, dt/5 for 5 cycle pulse
# Take the first derivative
#src = np.diff(src)/ dt
#src[nt - 1] = 0

#Fourier transform

spec = np.fft.fft(src) ## source time function in frequency domain

freq = np.fft.fftfreq(spec.size, d=dt ) # time domain to frequency domain
freq=2*freq*np.pi

#Applying Hilbert transform to the signal
comp_src0=hilbert(src)
phase0=np.angle(comp_src0)  #Calculate the angle of the signal, phase=np.angle(comp_src,deg=1) for gettting in degree


c0*dt/dx


src=src/30
src.max()


f2=plt.figure(figsize=(10, 12))
fig2=plt.subplot(221)
time = np.arange(nt) * dt
plt.plot(time, src)
plt.title('Source time function')
plt.xlabel('Time (s) ')
plt.ylabel('Source amplitude ')
plt.xlim(time[0], time[-100])

plt.subplot(222)
plt.title('Source spectrum')
plt.xlabel('Frequency(Hz) ')
plt.ylabel('Amplitude ')
plt.xlim(0, 1000)
plt.plot(np.abs(freq), np.abs(spec)) # plot frequency and amplitude

plt.subplot(223)
plt.plot(time, comp_src0.real, 'b-', time, comp_src0.imag, 'r--',time, abs(comp_src0), '-g')
plt.title('Hibert Transformed function')
plt.xlabel('Time (s) ')
plt.ylabel('Source amplitude ')
plt.legend(('real', 'imaginary','magnitude'))
plt.xlim(time[0], time[-100])

plt.subplot(224)
plt.plot(time, phase0)
plt.title('Plot of Phase')
plt.xlabel('Time (s) ')
plt.ylabel('Phase (rad) ')
plt.xlim(time[0], time[-100])

#plt.show()
plt.savefig("file1_2.png")


#Calculation to find the time of arrival
t0=np.argmax(abs(comp_src0))
t0


# Initialize pressure at different time steps and the second
# derivatives in each direction
p = np.zeros((nz, 2*nx))
pold = np.zeros((nz, 2*nx))
pnew = np.zeros((nz, 2*nx))
pxx = np.zeros((nz, 2*nx))
pzz = np.zeros((nz, 2*nx))

f = plt.figure(figsize=(8, 4));
sp =  f.add_subplot(1, 1, 1 );
#plt.axis([-xn/2,xn/2,0,zn/2])
plt.axis([-xn,xn,0,200])
#plt.text(0,40,'o')  #Plot the source 
for x, z in zip(irx, irz):
    plt.text(x, z, '+')
image = plt.imshow(pnew, interpolation='nearest', animated=True,extent =[-xn, xn,0, zn],vmin=-1, vmax=1, cmap=plt.cm.jet)
#plt.imshow(c,extent =[-nx, nx,0, nz])

plt.colorbar()
#plt.ion()
plt.savefig("file1_3.png")

# required for seismograms
seis = np.zeros((len(irx), nt))
ir = np.arange(len(irx))


# Time extrapolation
for it in range(nt):
    # calculate partial derivatives, be careful around the boundaries, nop,length of operator=5
    for i in range(2, 2*nx - 2):
        pzz[:, i] = -1./12*p[:,i+2]+4./3*p[:,i+1]-5./2*p[:,i]+4./3*p[:,i-1]-1./12*p[:,i-2]
    for j in range(2, nz - 2):
        pxx[j, :] = -1./12*p[j+2,:]+4./3*p[j+1,:]-5./2*p[j,:]+4./3*p[j-1,:]-1./12*p[j-2,:]
        
    pxx /= dx ** 2
    pzz /= dx ** 2
    # Time extrapolation
    pnew = 2 * p - pold +  (dt ** 2) * (c ** 2) * (pxx + pzz)
    # Add source term at isx, isz
    for i in range(2660):
        pnew[2250,i] = pnew[2250,i] + src[it] # deault (10,200)
#     for i in range(800):
#         pnew[300,i] = pnew[300,i] + src[it] # deault (10,200)


         
#     print(it*dt)
    # Plot every isnap-th iteration
    if it % 100 == 0:    # you can change the speed of the plot by increasing the plotting interval
        
        plt.title("Max P: %.4f" % p.max())
        image.set_data(pnew)
        #plt.savefig("%d file.png" %it)
        plt.gcf().canvas.draw()
        print(it*dt)
        #winsound.Beep(freqy, duration)

    pold, p = p, pnew

    # Save seismograms
    #seis[ir, it] = p[irz_d[ir],irx_d[ir]]



