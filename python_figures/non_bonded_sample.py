#backend = 'svg'
execfile('std_header.py')

data = {}
#M28
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 854")
data['M28'] = np.array(cursor.fetchall())
#M44
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 856")
data['M44'] =  np.array(cursor.fetchall())
#Temperature
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 861")
data['TEMPERATURE'] =  np.array(cursor.fetchall())

axis_array = []
fig = plt.figure()
fig.subplots_adjust(bottom=d.bottom_room) # Make room for x-label
fig.subplots_adjust(right=d.right_room) # Make room for second y-label
axis = fig.add_subplot(1,1,1)


axis.semilogy(data['M28'][:,0], data['M28'][:,1], 'r-')
axis.semilogy(data['M44'][:,0], data['M44'][:,1], 'g-')
#axis.set_ylim(0,0.5)
#axis_array[i].set_xlim(1100,0)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
axis.set_ylabel('Ion Current / nA', fontsize=d.y_axis_font)
axis.set_xlabel('Time / Minutes', fontsize=d.x_axis_font)


axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'k-')
axis2.set_ylabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)

plt.show()
#plt.savefig('../svg_figures/original_oscillation_zoom.svg')
