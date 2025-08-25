from patoPlot import *

# List of data files
region = "porousMat"
PATOFileList_=[]
PATOFileList_.append("../output/"+region+"/scalar/Ta_surfacePatch")
PATOFileList_.append("../output/"+region+"/scalar/Ta_plot")
PATOFileList_.append("../output/"+region+"/mass")
PATOFileList_.append("../output/"+region+"/massLoss")

# Read data files
patoPlot = patoPlot(PATOFileList_)

# Set up plot parameters
params = {
    'axes.labelsize': 14,
    'legend.fontsize': 14,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'text.usetex': False,
    'figure.figsize': [10, 5]
}
rcParams.update(params)

### Temperature ###
# Create figure
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# Create labels
ax.set_xlabel('Time (s)', fontsize=16)
ax.set_ylabel('Temperature (K)', fontsize=16)
tick_params(axis='x', top='off')
tick_params(axis='y', right='off')
# plot the data
data=patoPlot.dataList[0]
plot(data[:,0],data[:,1],ls='solid', color = "black",linewidth=2,label="Wall", alpha = 0.8)
data=patoPlot.dataList[1]
plot(data[:,0],data[:,1],ls='solid', color = "purple",linewidth=2,label="TC1", alpha = 0.8)
plot(data[:,0],data[:,2],ls='solid', color = "red",linewidth=2,label="TC2", alpha = 0.8)
plot(data[:,0],data[:,3],ls='solid', color = "blue",linewidth=2,label="TC3", alpha = 0.8)
plot(data[:,0],data[:,4],ls='solid', color = "green",linewidth=2,label="TC4", alpha = 0.8)
plot(data[:,0],data[:,5],ls='solid', color = "grey",linewidth=2,label="TC5", alpha = 0.8)
plot(data[:,0],data[:,6],ls='solid', color = "orange",linewidth=2,label="TC6", alpha = 0.8)
plot(data[:,0],data[:,7],ls='solid', color = "yellow",linewidth=2,label="TC7", alpha = 0.8)

#plt.axvline(1.00357, color='b', ls='--')
#plt.axvline(1.81912, color='b', ls='--')

plt.legend()
plt.tight_layout()
plt.grid()
outputFile_ = "Temperature.pdf"
plt.savefig(outputFile_)
plt.close(fig)

### Pyrolysis mass flux ### 
# Create figure 
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# Create labels 
ax.set_xlabel('Time (s)', fontsize=16)
ax.set_ylabel('$\dot{m}$ (kg/m2/s)', fontsize=16)
tick_params(axis='x', top='off')
tick_params(axis='y', right='off')
# plot the data 
data=patoPlot.dataList[2]
plot(data[:,0],data[:,1],ls='solid', color = "black",linewidth=2,label="$\dot{m}_g$", alpha = 0.8)
plot(data[:,0],data[:,2],ls='solid', color = "grey",linewidth=2,label="$\dot{m}_c$", alpha = 0.8)

plt.axvline(0.29, color='b', ls='--')
plt.axvline(0.49, color='b', ls='--')
plt.axvline(1.00, color='b', ls='--')
plt.axvline(1.68, color='b', ls='--')
plt.axvline(2.65, color='b', ls='--')
plt.axvline(5.42, color='b', ls='--')


plt.legend()
plt.tight_layout()
plt.grid()
outputFile_ = "MassFlux.pdf"
plt.savefig(outputFile_)
plt.close(fig)

### 98% virgin / 2% char / recession ### 
# Create figure
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# Create labels    
ax.set_xlabel('Time (s)', fontsize=16)
ax.set_ylabel('Depth (m)', fontsize=16)
tick_params(axis='x', top='off')
tick_params(axis='y', right='off')
# plot the data 
data=patoPlot.dataList[2]
plot(data[:,0],data[:,3],ls='solid', color = "black",linewidth=2,label="98% virgin", alpha = 0.8)
plot(data[:,0],data[:,4],ls='solid', color = "grey",linewidth=2,label="2% char", alpha = 0.8)
plot(data[:,0],data[:,5],ls='solid', color = "blue",linewidth=2,label="Recession", alpha = 0.8)

#plt.axvline(1.00357, color='b', ls='--')
#plt.axvline(2.81912, color='b', ls='--')


plt.legend()
plt.tight_layout()
plt.grid()
outputFile_ = "virgin_char_fronts.pdf"
plt.savefig(outputFile_)
plt.close(fig)


### t(s) Mean density(kg/m³), V/V0, m/m0

plt.figure()
data=patoPlot.dataList[3]
plt.plot(data[:, 0], data[:,1], label='Mean density')
#plt.axvline(1.00357, color='b', ls='--')
#plt.axvline(1.81912, color='b', ls='--')
plt.legend()
plt.grid()
plt.xlabel('Time (s)', fontsize=16)
plt.ylabel('Mean density (kg/m3)')
plt.tight_layout()
#plt.show()
plt.savefig('mean_density.pdf')
plt.close(fig)

plt.figure()
plt.plot(data[:, 0], data[:,2], label='V/V0')
#plt.axvline(1.00357, color='b', ls='--')
#plt.axvline(1.81912, color='b', ls='--')
plt.legend()
plt.grid()
plt.xlabel('Time (s)', fontsize=16)
plt.tight_layout()
#plt.show()
plt.savefig('volume_ratio.pdf')
plt.close(fig)

plt.figure()
data=patoPlot.dataList[3]
plt.plot(data[:, 0], data[:,3], label='m/m0')
#plt.axvline(1.00357, color='b', ls='--')
#plt.axvline(1.81912, color='b', ls='--')
plt.legend()
plt.grid()
plt.xlabel('Time (s)', fontsize=16)
plt.tight_layout()
#plt.show()
plt.savefig('mass_ratio.pdf')
plt.close(fig)

