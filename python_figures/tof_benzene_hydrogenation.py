backend = 'svg'
execfile('std_header.py')

#Mass of NH3: 17.0265491
#Mass of OH: 17.0027397

#Correct this expression to spectrum 403
def MassToTime(mass):
    time = 2.97277909899 * (mass**0.499352719883)
    corr_time = time + 0.153#Not adapted to 403
    corr_time = time + 0.220
    return corr_time 

    time = 2.98660484819 * (mass**0.4977024241071)
    corr_time = time + 0.153
    return corr_time 


fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room) 
fig.subplots_adjust(hspace=0.2)

ratio = 0.8
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)


data = {}
#Benzene in He
cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = 323")
data['pure'] = np.array(cursor.fetchall())
#Benzene in He
cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = 324")
data['hydrogen'] = np.array(cursor.fetchall())

axis_array = []

LINEWIDTH = 0.5
arrow = dict(facecolor='black',arrowstyle='->')
font = d.arrowfont

gs = gridspec.GridSpec(2, 3)
gs.update(wspace=0.2,hspace=0.4)

axis = plt.subplot(gs[0, :])

axis.plot(data['pure'][:,0], data['pure'][:,1], 'r-',linewidth=LINEWIDTH)
axis.plot(data['hydrogen'][:,0], data['hydrogen'][:,1], 'b-',linewidth=LINEWIDTH)
axis.set_xlim(0,28)
axis.set_xticks([5,10,15,20,25])

mass_ticks = np.array([1,2,5,10,20,30,40,50,60,70,80])
axis3 = axis.twiny()
axis3.set_xlim(0,28)
print MassToTime(2*1.0078250320)
axis3.set_xticks(MassToTime(mass_ticks))
axis3.set_xticklabels(mass_ticks)
axis3.set_xlabel('Mass / amu', fontsize=d.x_axis_font)
axis3.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
for tl in axis3.get_xticklabels():
    tl.set_size(8)

#axis3.ticklabel_format(useOffset=False)
axis.set_ylim(-10,450)
axis.set_yticks((0,100,200,300,400))

p = axis.axvspan(26, 27.7, facecolor='#26aaf7', alpha=0.25)
#p = axis.axvspan(15, 20, facecolor='#25dd37', alpha=0.25)
#p = axis.axvspan(26, 27.7, facecolor='#b6fa77', alpha=0.25)

axis.set_ylabel('Response / mV', fontsize=d.y_axis_font)
#axis.set_xlabel('Flight Time / $\mu$s', fontsize=d.y_axis_font)
axis.set_xlabel('')
axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)


"""
axis = plt.subplot(gs[1,0])
axis.set_ylabel('Response / mV', fontsize=d.y_axis_font)
axis.set_yticks((0,50,100,150,200))
axis.plot(data['pure'][:,0], data['pure'][:,1], 'r-',linewidth=LINEWIDTH)
axis.plot(data['hydrogen'][:,0], data['hydrogen'][:,1], 'b-',linewidth=LINEWIDTH)
p = axis.axvspan(0, 1, facecolor='#26aaf7', alpha=0.25)
axis.set_xlim(4.35,4.45)
axis.set_ylim(0,225)
axis.set_xticks([4.35,4.4,4.45])
axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

axis = plt.subplot(gs[1,1])
axis.set_ylabel('')
axis.set_yticks((10,20,30,40,50,60,70,80,90))
#axis.set_xticks((3.25,3.75,4.25))
axis.plot(data['pure'][:,0], data['pure'][:,1], 'r-',linewidth=LINEWIDTH)
axis.plot(data['hydrogen'][:,0], data['hydrogen'][:,1], 'b-',linewidth=LINEWIDTH)
p = axis.axvspan(3.0, 4.5, facecolor='#25dd37', alpha=0.25)
axis.set_xlim(15,20)
axis.set_ylim(0,100)
axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis.ticklabel_format(useOffset=False)
#axis.annotate('H', xy=(3.2, 10),  xycoords='data', xytext=(3.5, 15), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
#axis.annotate('H$_2$', xy=(4.35, 10),  xycoords='data', xytext=(4.2, 20), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.set_xlabel('Flight Time / $\mu$s', fontsize=d.x_axis_font)
"""

#axis = plt.subplot(gs[1,2])
axis = plt.subplot(gs[1,:])
axis.set_ylabel('')
axis.set_yticks((50,100,150,200,250,300,350,400,450))
#axis.set_xticks((12,12.5))
axis.plot(data['pure'][:,0], data['pure'][:,1], 'r-',linewidth=LINEWIDTH)
axis.plot(data['hydrogen'][:,0], data['hydrogen'][:,1], 'b-',linewidth=LINEWIDTH)
axis.set_xlim(26,27.7)
axis.set_ylim(-10,450)

#axis.set_xticks([12.1,12.2,12.3,12.4])
axis.ticklabel_format(useOffset=False)
#p = axis.axvspan(26, 27.7, facecolor='#b6fa77', alpha=0.25)
axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

mass_ticks = np.array([76,77,78,79,80,81,82,83,84,85])
axis3 = axis.twiny()
axis3.set_xlim(26,27.7)
print MassToTime(2*1.0078250320)
axis3.set_xticks(MassToTime(mass_ticks))
axis3.set_xticklabels(mass_ticks,size=60)

axis3.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='x',pad=d.pad)
for tl in axis3.get_xticklabels():
    tl.set_size(8)

axis.set_yticks((0,100,200,300,400))
axis.set_ylabel('Response / mV', fontsize=d.y_axis_font)
axis.set_xlabel('Flight Time / $\mu$s', fontsize=d.y_axis_font)

#axis.annotate('O', xy=(12.04, 10),  xycoords='data', xytext=(12.04, 67), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
#axis.annotate('NH$_2$', xy=(12.055, 47),  xycoords='data', xytext=(12.2, 75), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
#axis.annotate('OH', xy=(12.414, 50),  xycoords='data', xytext=(12.35, 66), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
#axis.annotate('NH$_3$', xy=(12.425, 85),  xycoords='data', xytext=(12.35, 130), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)


#plt.tight_layout()
#plt.show()
plt.savefig('../svg_figures/tof_benzene_hydrogenation.svg')
