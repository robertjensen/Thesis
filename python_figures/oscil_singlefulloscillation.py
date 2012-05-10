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
axis.set_ylim(0.1,1.2)
axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
axis2.set_ylim(160,205)
axis2.set_yticks((170,180,190,200))
axis.set_xlim(1001,1133)
axis.grid(False)    

#arrow = dict(facecolor='black', shrink=0.085,width=1)
arrow = dict(facecolor='black',arrowstyle='->')
axis.annotate('CO', xy=(1040, 0.82),  xycoords='data', xytext=(1055, 0.85), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=9,)
axis.annotate('CO$_2$', xy=(1040, 0.5),  xycoords='data', xytext=(1050, 0.65), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=9,)
axis.annotate('Temp.', xy=(1070, 1.08),  xycoords='data', xytext=(1095, 0.93), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=9,)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis2.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

axis.set_ylabel('SEM Current / nA', fontsize=d.y_axis_font)
axis2.set_ylabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)
axis.set_xlabel('Time / min', fontsize=d.x_axis_font)


positions = []
positions.append([.18, .2, .15, .15])
positions.append([.29, .2, .15, .15])
positions.append([.39, .2, .15, .15])
positions.append([.5,  .2, .15, .15])
positions.append([.6,  .2, .15, .15])
positions.append([.69, .2, .15, .15])

oxide = []
oxide.append([0.001,3.14])
oxide.append([1,0])
oxide.append([0.7,0.5])
oxide.append([0.5,1])
oxide.append([0.2,1.5])
oxide.append([0.001,3.14])

N = 500
R = np.random.rand(N)
Theta = np.random.rand(N)*2*np.pi
area = 0.8
colors = np.zeros((N,len(positions)))

j = 0
for pos in positions:
    a = plt.axes(pos, axisbg='w',polar=True)
    print oxide[j][0]
    for i in range(0,N):
        if (R[i]>oxide[j][0]) and ((Theta[i] < oxide[j][1]) or (Theta[i] > 2*np.pi - oxide[j][1])):
            colors[i][j] = 1
            
    c = plt.scatter(Theta, R, c=colors[:,j], s=area, linewidths=0)
    c.set_alpha(0.75)
    plt.setp(a, xticks=[], yticks=[])
    j = j + 1



#plt.tight_layout()
plt.show()
plt.savefig('../svg_figures/oscil_single_full.svg')
