backend = 'svg'
execfile('std_header.py')

import sensitivity_parameters as sens_parm

p = sens_parm.N8_up

data = {}
#N8
#O2
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 457 and x between " + p.xlow + " and " + p.xhigh)
data['M32'] =  np.array(cursor.fetchall())
#CO2
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 458 and x between " + p.xlow + " and " + p.xhigh)
data['M44'] =  np.array(cursor.fetchall())
#Temperature
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 463")
data['TEMPERATURE'] =  np.array(cursor.fetchall())


temp_interp = interpolate.interp1d(data['TEMPERATURE'][:,0],data['TEMPERATURE'][:,1], bounds_error=False)
m32_interp = interpolate.interp1d(data['M32'][:,0],data['M32'][:,1], bounds_error=False)
m44_interp = interpolate.interp1d(data['M44'][:,0],data['M44'][:,1], bounds_error=False)

oxygen_factor = 8.2e-3
bg = 0.12

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room) 
fig.subplots_adjust(hspace=0.3)

ratio = 1
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

axis = fig.add_subplot(2,1,1)

axis.plot(temp_interp(data['M44'][:,0]), data['M44'][:,1], 'g-')
axis.plot(temp_interp(data['M44'][:,0]), data['M44'][:,1]-oxygen_factor*m32_interp(data['M44'][:,0]), 'b-')
axis.plot(temp_interp(data['M44'][:,0]), data['M44'][:,1]-bg-oxygen_factor*m32_interp(data['M44'][:,0]), 'k-')
axis.set_yscale('log')

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
axis.set_xlabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)
axis.set_ylabel('SEM Current / nA', fontsize=d.y_axis_font)
axis.set_xlim(50,400)
axis.set_ylim(1e-2,12)

arrow = dict(facecolor='black',arrowstyle='->')
font = d.arrowfont
axis.annotate('Original', xy=(250, 0.5),  xycoords='data', xytext=(220, 2), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('BG Corrected', xy=(110, 0.08),  xycoords='data', xytext=(140, 0.3), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('BG + offset corrected', xy=(270, 0.15),  xycoords='data', xytext=(360, 0.04), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)

axis = fig.add_subplot(2,1,2)

axis.plot(1000.0/(273.15+temp_interp(data['M44'][:,0])), data['M44'][:,1], 'g-')
axis.plot(1000.0/(273.15+temp_interp(data['M44'][:,0])), data['M44'][:,1]-oxygen_factor*m32_interp(data['M44'][:,0]), 'b-')
axis.plot(1000.0/(273.15+temp_interp(data['M44'][:,0])), data['M44'][:,1]-bg-oxygen_factor*m32_interp(data['M44'][:,0]), 'k-')
axis.set_yscale('log')

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
axis.set_xlabel('1000K / Temperature', fontsize=d.y_axis_font)
axis.set_ylabel('SEM Current / nA', fontsize=d.y_axis_font)
axis.set_xlim(1.5,3)
axis.set_ylim(1e-2,12)

arrow = dict(facecolor='black',arrowstyle='->')
font = d.arrowfont
axis.annotate('Original', xy=(2.2, 0.5),  xycoords='data', xytext=(2.6, 2), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('BG Corrected', xy=(2.6, 0.08),  xycoords='data', xytext=(2.9, 0.4), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('BG + offset corrected', xy=(2, 0.06),  xycoords='data', xytext=(2.8, 0.03), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)


#plt.show()
plt.savefig('../svg_figures/sensitivity_background_correction.svg')
