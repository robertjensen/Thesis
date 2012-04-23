backend = 'svg'
execfile('std_header.py')

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room) 

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

axis_array = []

for i in range(0,1):
    axis_array.append(fig.add_subplot(1,1,i+1))
    axis_array[i].plot(data['M28'][:,0], data['M28'][:,1], 'r-')
    axis_array[i].plot(data['M44'][:,0], data['M44'][:,1], 'b-')
    axis_array[i].set_ylim(0,0.5)
    #axis_array[i].set_xlim(1100,0)
    
    
    axis_array[i].tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
axis_array[0].set_ylabel('Ion Current / nA', fontsize=d.y_axis_font)
axis_array[0].set_xlabel('Time / Minutes', fontsize=d.x_axis_font)

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

for i in range(0,2):
    axis_array.append(fig.add_subplot(2,1,i+1))
    axis_array[i].plot(data['M28'][:,0], data['M28'][:,1], 'r-')
    axis_array[i].plot(data['M44'][:,0], data['M44'][:,1], 'b-')
    axis_array[i].set_ylim(0,0.5)
    axis_array[i].set_xlim(xlim[i])
    
    
    axis_array[i].tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
axis_array[0].set_ylabel('Ion Current / nA', fontsize=d.y_axis_font)
axis_array[1].set_ylabel('Ion Current / nA', fontsize=d.y_axis_font)
axis_array[0].set_xlabel('Time / Minutes', fontsize=d.x_axis_font)
axis_array[1].set_xlabel('Time / Minutes', fontsize=d.x_axis_font)
#plt.show()
plt.savefig('../svg_figures/original_oscillation_zoom.svg')