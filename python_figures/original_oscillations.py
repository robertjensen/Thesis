backend = 'svg'
execfile('std_header.py')

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room*0.95) 

ratio = d.ratio
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

data = {}
#M28
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactor where measurement = 5849")
data['M28'] = np.array(cursor.fetchall())
#M44
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactor where measurement = 5853")
data['M44'] =  np.array(cursor.fetchall())
#Temp
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 5859")
data['TEMPERATURE'] =  np.array(cursor.fetchall())

axis = fig.add_subplot(1,1,1)
axis.plot(data['M28'][:,0], data['M28'][:,1], 'r-')
axis.plot(data['M44'][:,0], data['M44'][:,1], 'g-')
axis.set_ylim(0,0.5)
#axis.set_xlim(1100,0)
axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
#axis2.set_ylim(0,300)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
axis.set_ylabel('SEM Current / nA', fontsize=d.y_axis_font)
axis2.set_ylabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)
axis.set_xlabel('Time / Minutes', fontsize=d.x_axis_font)

arrow = dict(facecolor='black',arrowstyle='->')
axis.annotate('CO', xy=(700, 0.34),  xycoords='data', xytext=(640, 0.42), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('CO$_2$', xy=(500, 0.28),  xycoords='data', xytext=(375, 0.3), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('Temp.', xy=(450, 0.36),  xycoords='data', xytext=(275, 0.41), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)

#plt.tight_layout()
#plt.show()
plt.savefig('../svg_figures/original_oscillation.svg')


axis_array = []



fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room) 

ratio = d.ratio
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)



xlim = [(900,1000),(950,980)]
xticks = [(920,940,960,980),(955,960,965,970,975)]
for i in range(0,2):
    axis_array.append(fig.add_subplot(2,1,i+1))
    axis_array[i].plot(data['M28'][:,0], data['M28'][:,1], 'r-')
    axis_array[i].plot(data['M44'][:,0], data['M44'][:,1], 'g-')
    axis_array[i].set_ylim(0,0.5)
    axis_array[i].set_xlim(xlim[i])
    axis_array[i].set_xticks(xticks[i])
    axis_array[i].set_yticks((0.1,0.2,0.3,0.4))
    
    axis_array[i].tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
axis_array[0].set_ylabel('I$_{SEM}$ / nA', fontsize=d.y_axis_font)
axis_array[1].set_ylabel('I$_{SEM}$ / nA', fontsize=d.y_axis_font)
#axis_array[0].set_xlabel('Time / Minutes', fontsize=d.x_axis_font)
axis_array[1].set_xlabel('Time / Minutes', fontsize=d.x_axis_font)
#plt.show()
plt.savefig('../svg_figures/original_oscillation_zoom.svg')