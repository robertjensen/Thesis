backend = 'svg'
execfile('std_header.py')

data = {}
#CO
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 456")
data['M28'] =  np.array(cursor.fetchall())
#O2
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 457")
data['M32'] =  np.array(cursor.fetchall())
#CO2
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 458")
data['M44'] =  np.array(cursor.fetchall())

#Temperature
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 463")
data['TEMPERATURE'] =  np.array(cursor.fetchall())

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

axis.plot(data['M28'][:,0], data['M28'][:,1], 'r-')
axis.plot(data['M32'][:,0], data['M32'][:,1], 'k-')
axis.plot(data['M44'][:,0], data['M44'][:,1], 'g-')

#axis.set_yscale('log')

axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')

#axis.set_ylim(0,0.5)
axis.set_xlim(0,445)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
axis.set_xlabel('Time / min', fontsize=d.y_axis_font)
axis.set_ylabel('SEM Current / nA', fontsize=d.y_axis_font)
axis2.set_ylabel('Temperaturet / $^\circ$C', fontsize=d.y_axis_font)
#axis.set_xticklabels([])

arrow = dict(facecolor='black',arrowstyle='->')
font = d.arrowfont
axis.annotate('O$_2$', xy=(160, 53),  xycoords='data', xytext=(140, 45), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('CO', xy=(150, 26),  xycoords='data', xytext=(112, 34), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('CO$_2$', xy=(275, 11),  xycoords='data', xytext=(302, 23), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('Temp.', xy=(296, 70),  xycoords='data', xytext=(370, 76), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)


plt.show()
plt.savefig('../svg_figures/sensitivity_procedure.svg')
