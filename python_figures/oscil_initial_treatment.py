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
fig.subplots_adjust(right=d.right_room*0.95) 

ratio = d.ratio*1.3
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

gs = gridspec.GridSpec(2, 2)

gs.update(wspace=0.1,hspace=0.4)

axis = plt.subplot(gs[0, :])
#axis = fig.add_subplot(2,2,1)

p = axis.axvspan(460, 490, facecolor='#b6fa77', alpha=0.25)
p = axis.axvspan(710, 740, facecolor='#28cfe9', alpha=0.35)
axis.plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
axis.plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'g-')
axis.set_ylim(0,8)
axis.set_yticks((2,4,6))
axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
axis2.set_ylim(0,300)
axis2.set_yticks((50,150,250))
axis.set_xlim(250,800)
axis.grid(False)    



#arrow = dict(facecolor='black', shrink=0.085,width=1)
arrow = dict(facecolor='black',arrowstyle='->')
axis.annotate('CO', xy=(375, 2.4),  xycoords='data', xytext=(350, 1.1), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('CO$_2$', xy=(420, 3.7),  xycoords='data', xytext=(460, 5.4), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('Temp.', xy=(440, 6.6),  xycoords='data', xytext=(380, 7.2), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis2.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

axis.set_ylabel('SEM Current / nA', fontsize=d.y_axis_font)
axis2.set_ylabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)
axis.set_xlabel('Time / min', fontsize=d.x_axis_font)



axis = plt.subplot(gs[1,0])
p = axis.axvspan(460, 490, facecolor='#b6fa77', alpha=0.25)
axis.plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
axis.plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'g-')
axis.set_ylim(0,6)
axis.set_yticks((1,3,5))
axis.text(463,1.2,"CO",fontsize=d.arrowfont,)
axis.text(465,2.3,"CO$_2$",fontsize=d.arrowfont,)
axis.text(470,4.9,"Temp.",fontsize=d.arrowfont,)
axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
axis2.set_ylim(0,300)
#axis2.set_yticks((170,180,190,200))
axis.set_xlim(460,490)
axis.set_ylabel('SEM Curr. / nA', fontsize=d.y_axis_font)
axis2.set_ylabel('', fontsize=d.y_axis_font)
axis.set_xticks((465,475,485))
axis2.set_yticks(())
axis.set_xlabel('Time / min', fontsize=d.x_axis_font)
axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis2.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

axis.grid(False)

axis = plt.subplot(gs[1,1])
#axis = fig.add_subplot(2,2,1)
p = axis.axvspan(710, 740, facecolor='#28cfe9', alpha=0.35)
axis.plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
axis.plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'g-')
axis.set_ylim(0,6)
axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
axis2.set_ylim(0,300)
axis2.set_yticks((50,150,250))
axis.set_xticks((715,725,735))
axis.text(715,0.8,"CO",fontsize=d.arrowfont,)
axis.text(722,3.4,"CO$_2$",fontsize=d.arrowfont,)
axis.text(718,4.3,"Temp.",fontsize=d.arrowfont,)
axis.set_xlim(710,740)
axis.set_yticks(())
axis2.set_ylabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)
axis.set_xlabel('Time / min', fontsize=d.x_axis_font)
axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis2.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

axis.grid(False)

#plt.tight_layout()
#plt.show()
plt.savefig('../svg_figures/oscil_initial_treatment.svg')
