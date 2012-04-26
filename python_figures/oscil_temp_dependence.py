backend = 'svg'
execfile('std_header.py')

data = {}
#Mass28
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 572")
data['M28'] = np.array(cursor.fetchall())

#Mass44
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 573")
data['M44'] =  np.array(cursor.fetchall())

#Temperature
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 578")
data['TEMPERATURE'] = np.array(cursor.fetchall())

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
axis.plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
axis.plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'g-')
axis.set_ylim(0.1,1.3)
axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
axis2.set_ylim(150,210)
#axis2.set_yticks((170,180,190,200))
axis.set_xlim(700,1000)
axis.grid(False)    

arrow = dict(facecolor='black',arrowstyle='->')
#arrow = dict(facecolor='black', shrink=0.085,width=1)
axis.annotate('CO', xy=(830, 0.85),  xycoords='data', xytext=(800, 0.95), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('CO$_2$', xy=(830, 0.4),  xycoords='data', xytext=(800, 0.25), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('Temp.', xy=(855, 1.15),  xycoords='data', xytext=(810, 1.2), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis2.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

axis.set_ylabel('SEM Current / nA', fontsize=d.y_axis_font)
axis2.set_ylabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)
axis.set_xlabel('Time / min', fontsize=d.x_axis_font)

#plt.tight_layout()
#plt.show()
plt.savefig('../svg_figures/oscil_temp_dependence.svg')
