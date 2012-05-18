backend = 'svg'
execfile('std_header.py')

import sensitivity_parameters as sens_parm

parameters = sens_parm.parameters

data = {}

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room) 
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.1)

ratio = 1
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

oxygen_factor = 8.2e-3
bg = 0.12

for i in range(0,len(parameters)):
    p = parameters[i]
    print p.name
    cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = " + p.m32 + " and x between " + p.xlow + " and " + p.xhigh)
    data['M32'] =  np.array(cursor.fetchall())
    cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = " + p.m44 + " and x between " + p.xlow + " and " + p.xhigh)
    data['M44'] =  np.array(cursor.fetchall())
    cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = " + p.temperature)
    data['TEMPERATURE'] =  np.array(cursor.fetchall())

    temp_interp = interpolate.interp1d(data['TEMPERATURE'][:,0],data['TEMPERATURE'][:,1], bounds_error=False)
    m32_interp = interpolate.interp1d(data['M32'][:,0],data['M32'][:,1], bounds_error=False)
    m44_interp = interpolate.interp1d(data['M44'][:,0],data['M44'][:,1], bounds_error=False)

    axis = fig.add_subplot(4,2,i+1)

    axis.plot(1000.0/(273.15+temp_interp(data['M44'][:,0])), data['M44'][:,1], 'g-')
    axis.plot(1000.0/(273.15+temp_interp(data['M44'][:,0])), data['M44'][:,1]-oxygen_factor*m32_interp(data['M44'][:,0]), 'b-')
    axis.plot(1000.0/(273.15+temp_interp(data['M44'][:,0])), data['M44'][:,1]-bg-oxygen_factor*m32_interp(data['M44'][:,0]), 'k-')
    axis.axvline(x=1000.0/(273.15+temp_interp(p.fitx[0]/60000)),color='k')
    axis.axvline(x=1000.0/(273.15+temp_interp(p.fitx[1]/60000)),color='k')
    axis.set_yscale('log')

    if i == 4:
        axis.set_ylabel('SEM Current / nA', fontsize=d.y_axis_font)
        
    if i%2 == 1:
        axis.set_ylabel('')
        axis.set_yticks(())
        axis2 = axis.twinx()
        axis2.set_xticks(())
        axis2.set_yscale('log')
        axis2.set_ylabel('')
        axis2.set_ylim(1e-2,20)
        axis2.set_yticks((10,1,0.1))
        axis2.set_yticklabels(('10','1','0.1'))
        axis2.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    else:
        axis.set_yticks((10,1,0.1))
        axis.set_yticklabels(('10','1','0.1'))
        
    if i>5:
        axis.set_xlabel('1000K / Temperature', fontsize=d.y_axis_font)
        axis.set_xticks((1.5,2,2.5,3))
    else:
        axis.set_xlabel('')
        axis.set_xticks(())

    axis.set_xlim(1.4,3)
    axis.set_ylim(1e-2,20)
    axis.annotate(p.name, (0.6,0.75),xycoords='axes fraction',fontsize=d.arrowfont-1)
    axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

#plt.show()
plt.savefig('../svg_figures/sensitivity_background_correction_complete.svg')