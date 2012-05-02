backend = 'svg'
execfile('std_header.py')

data = {}
#Flow O2
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6981")
data['O2'] = np.array(cursor.fetchall())
#Flow CO
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6982")
data['CO'] =  np.array(cursor.fetchall())
#Flow He
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6983")
data['He'] =  np.array(cursor.fetchall())
#Flow He
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6978")
data['pressure'] =  np.array(cursor.fetchall())
#Temperature
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6980")
data['TEMPERATURE'] =  np.array(cursor.fetchall())
#Mass 44
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactor where measurement = 6976")
data['M44'] =  np.array(cursor.fetchall())



fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room) 

ratio = 0.9
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

gs = gridspec.GridSpec(3, 1)
axis = plt.subplot(gs[0:2, 0])

axis.plot(data['O2'][:,0], data['O2'][:,1], 'm-')
axis.plot(data['CO'][:,0], data['CO'][:,1], 'r-')
axis.plot(data['He'][:,0], data['He'][:,1], 'c-')
#axis.plot(data['pressure'][:,0], data['pressure'][:,1], 'k-')
#axis.set_ylim(0,0.5)
axis.set_xlim(0,120)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
axis.set_ylabel('Flow / mL/min', fontsize=d.y_axis_font)
axis.set_xticklabels([])

arrow = dict(facecolor='black',arrowstyle='->')
font = d.arrowfont
axis.annotate('O$_2$', xy=(12, 5),  xycoords='data', xytext=(19, 6.4), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('CO', xy=(80, 1),  xycoords='data', xytext=(85, 2.5), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('He', xy=(40, 5),  xycoords='data', xytext=(33, 5.75), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('Temp.', xy=(100, 6.5),  xycoords='data', xytext=(90, 5.5), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)

axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
axis2.set_ylabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)
axis2.set_xlim(0,120)
axis2.set_xticklabels([])
axis2.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

axis = plt.subplot(gs[2, 0])
axis.plot(data['M44'][:,0], data['M44'][:,1], 'g-')
axis.set_xlabel('Time / Minutes', fontsize=d.x_axis_font)
axis.set_xlim(0,120)
axis.set_ylabel('CO$_2$ / nA', fontsize=d.y_axis_font)
axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis2 = axis.twinx()
axis2.plot(data['pressure'][:,0], data['pressure'][:,1], 'k-')
axis2.set_ylabel('Reactor pressure / bar', fontsize=d.y_axis_font)
axis2.set_xlim(0,120)
axis2.set_ylim(0,1.1)
axis2.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

plt.show()
plt.savefig('../svg_figures/area_procedure.svg')
