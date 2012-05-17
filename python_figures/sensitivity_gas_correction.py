backend = 'svg'
execfile('std_header.py')

data = {}
#CO2
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 458 and x between 9200000 and 16400000")
data['M44'] =  np.array(cursor.fetchall())
#Chamber pressure
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 459 and x between 9200000 and 16400000")
data['PRESSURE'] =  np.array(cursor.fetchall())

#Temperature
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 463 and x between 9200000 and 16400000")
data['TEMPERATURE'] =  np.array(cursor.fetchall())

temp_interp = interpolate.interp1d(data['TEMPERATURE'][:,0],data['TEMPERATURE'][:,1], bounds_error=False)
x_data = data['M44'][:,0]
y_data = data['M44'][:,1]

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room*0.95) 

ratio = d.ratio
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

axis = fig.add_subplot(1,1,1)


#axis.plot(data['M44'][:,0], data['M44'][:,1], 'g-')
axis.plot(temp_interp(x_data), y_data, 'g-')
#axis.set_yscale('log')

axis2 = axis.twinx()
#axis2.plot(data['PRESSURE'][:,0], data['PRESSURE'][:,1], 'k-')
axis2.plot(temp_interp(data['PRESSURE'][:,0]), data['PRESSURE'][:,1], 'k-')

#axis.set_ylim(0,0.5)
axis.set_xlim(0,400)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
axis.set_xlabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)
axis.set_ylabel('SEM Current / nA', fontsize=d.y_axis_font)
axis2.set_ylabel('Chamber pressure / mbar', fontsize=d.y_axis_font)
#axis.set_xticklabels([])

arrow = dict(facecolor='black',arrowstyle='->')
font = d.arrowfont
axis.annotate('CO$_2$', xy=(345, 7e-9),  xycoords='data', xytext=(300, 9e-9), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('Pressure', xy=(80, 7e-9),  xycoords='data', xytext=(90, 5.3e-9), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)


plt.show()
plt.savefig('../svg_figures/sensitivity_gas_correction.svg')
