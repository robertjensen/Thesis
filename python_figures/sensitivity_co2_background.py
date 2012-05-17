#backend = 'svg'
execfile('std_header.py')

data = {}
#CO
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 456 and x<9000000")
data['M28'] =  np.array(cursor.fetchall())
#O2
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 457 and x<9000000")
data['M32'] =  np.array(cursor.fetchall())
#CO2
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 458 and x<9000000")
data['M44'] =  np.array(cursor.fetchall())

#Temperature
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 463")
data['TEMPERATURE'] =  np.array(cursor.fetchall())

temp_interp = interpolate.interp1d(data['TEMPERATURE'][:,0],data['TEMPERATURE'][:,1], bounds_error=False)
m28_interp = interpolate.interp1d(data['M28'][:,0],data['M28'][:,1], bounds_error=False)
m32_interp = interpolate.interp1d(data['M32'][:,0],data['M32'][:,1], bounds_error=False)
m44_interp = interpolate.interp1d(data['M44'][:,0],data['M44'][:,1], bounds_error=False)
x_data = data['M44'][:,0]

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room) 

ratio = d.ratio
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

axis = fig.add_subplot(1,1,1)

#axis.plot(x_data*60, (m44_interp(x_data)-0.1)/m28_interp(x_data), 'g-')
#axis.plot(x_data*60, (m44_interp(x_data)-0.1)/m32_interp(x_data), 'k-')
axis.plot(data['M32'][:,0], data['M32'][:,1], 'k-')
axis.plot(data['M28'][:,0], data['M28'][:,1], 'r-')
axis.plot(data['M44'][:,0], data['M44'][:,1], 'g-')
axis.set_yscale('log')


#axis2 = axis.twinx()
#axis2.set_yscale('log')

axis.set_ylim(0.09,100)
axis.set_xlim(0,150)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
axis.set_xlabel('Time / min', fontsize=d.y_axis_font)
axis.set_ylabel('SEM Current / nA', fontsize=d.y_axis_font)
#axis2.set_ylabel('Temperaturet / $^\circ$C', fontsize=d.y_axis_font)
#axis.set_xticklabels([])

arrow = dict(facecolor='black',arrowstyle='->')
font = d.arrowfont
axis.annotate('O$_2$', xy=(89, 60),  xycoords='data', xytext=(110, 48), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('CO', xy=(114, 13),  xycoords='data', xytext=(102, 15), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('CO$_2$', xy=(98, 0.5),  xycoords='data', xytext=(85, 0.8), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)


plt.show()
plt.savefig('../svg_figures/sensitivity_co2_background.svg')
