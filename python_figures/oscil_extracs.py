backend = 'svg'
execfile('std_header.py')

data = {}
#Mass28
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6133")
data['M28'] = np.array(cursor.fetchall())

#Mass44
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6135")
data['M44'] =  np.array(cursor.fetchall())

#Temperature
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6139")
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

axis_array = []
axis2_array = []

limit = []
#limit.append((700,900))
limit.append((700,800))
#limit.append((2800,3000))
limit.append((2800,2900))
#limit.append((5800,6000))
limit.append((5900,6000))

for i in range(0,3):
    axis_array.append(fig.add_subplot(3,1,i+1))
    axis_array[i].plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
    axis_array[i].plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'g-')
    axis_array[i].set_ylim(0,7)
    axis2_array.append(axis_array[i].twinx())
    axis2_array[i].plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
    axis2_array[i].set_ylim(181,229)
    axis_array[i].set_xlim(limit[i])
    axis_array[i].set_yticks((1,3,5))
    
    axis_array[i].tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    axis2_array[i].tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    axis_array[i].grid(False)    

arrow = dict(facecolor='black',arrowstyle='->')
axis_array[0].annotate('CO', xy=(710, 3.9),  xycoords='data', xytext=(710, 5.7), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis_array[0].annotate('CO$_2$', xy=(725, 1.7),  xycoords='data', xytext=(715, 0.5), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis_array[0].annotate('T', xy=(728, 4.9),  xycoords='data', xytext=(720, 5.3), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)

axis_array[1].set_ylabel('SEM Current / nA', fontsize=d.y_axis_font)
axis2_array[1].set_ylabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)
axis_array[2].set_xlabel('Time / min', fontsize=d.x_axis_font)


#plt.tight_layout()
#plt.show()
plt.savefig('../svg_figures/oscil_extracts.svg')
