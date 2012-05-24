backend = 'svg'
execfile('std_header.py')

data = {}
#Mass28
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6694")
data['M28'] = np.array(cursor.fetchall())

#Mass44
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6696")
data['M44'] =  np.array(cursor.fetchall())

#CO Flow
cursor.execute("SELECT x/60000,y FROM xy_values_microreactor where measurement = 6702")
data['CO_FLOW'] = np.array(cursor.fetchall())


i = 0
old_flow = 0
flow_sections = [] #Holds the times of the concentrations steps
concentrations = [] #Holds the actual concentration
for row in data['CO_FLOW']:
    i = i+1
    if (row[1] > (old_flow + 0.04)):
        flow_sections.append(row[0])
        concentrations.append(row[1])
        old_flow = row[1]
        
    if (i%10==0):
        old_flow = row[1]

steps = len(flow_sections)

concentrations.append(100000) #Final point
flow_sections.append(1000000)

#Limit: everytime the concentration-corrected M44 goes above 0.5nA we start a new oscillation
i = 0
j = 0
old_ccc = 0
oscillations = [] #Holds the switching times
for row in data['M44']:
    if row[0]>flow_sections[j]:
        j = j+1
    i = i+1
    ccc = 1e9 * row[1] / concentrations[j] # ccc = Concentrations Corrected Current
    if (ccc > (0.5)) and (old_ccc<0.5):
        oscillations.append(row[0])
        old_ccc = ccc
        
    if (i%5==0):
        old_ccc = ccc




periods = []
periods.append(0)
for i in range(1,len(oscillations)):
    periods.append(oscillations[i]-oscillations[i-1])


fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room*0.95) 

ratio = d.ratio
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)


print len(oscillations)
print len(periods)

axis = fig.add_subplot(1,1,1)
axis.plot(oscillations, periods, 'b.')
#axis.plot(data['M28'][:,0], data['M28'][:,1], 'r-')
#axis.plot(data['M44'][:,0], data['M44'][:,1], 'b-')
axis.set_ylim(0,50)
axis.set_xlim(0,3100)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis.grid(False)    

axis.set_ylabel('Oscillation period / minutes', fontsize=d.y_axis_font)
axis.set_xlabel('Time / min', fontsize=d.x_axis_font)

axis2 = axis.twinx()
#axis2.plot(data['CO_FLOW'][:,0], data['CO_FLOW'][:,1], 'r-')
axis2.plot(data['CO_FLOW'][:,0], data['CO_FLOW'][:,1]/(4+data['CO_FLOW'][:,1]), 'k-')
axis2.set_xlim(0,3100)
axis2.set_ylim(0,0.15)
axis2.set_ylabel('CO/O$_2$-ratio', fontsize=d.y_axis_font)    
#axis2.set_yticks((0.025,0.05,0.075,0.1,0.125))
axis2.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)



#plt.tight_layout()
plt.show()
plt.savefig('../svg_figures/oscil_gas_dep_sum.svg')



##fig = plt.figure()
##axis_array = []
##axis2_array = []
##
##for i in range(0,steps-1):
##    axis_array.append(fig.add_subplot((steps-1)/2,2,i+1))
##    axis_array[i].plot(data['M28'][:,0], data['M28'][:,1]*1e9/concentrations[i], 'r-')
##    axis_array[i].plot(data['M44'][:,0], data['M44'][:,1]*1e9/concentrations[i], 'b-')
##    axis_array[i].set_ylim(0,2)
##    axis2_array.append(axis_array[i].twinx())
##    axis2_array[i].plot(data['CO_FLOW'][:,0], data['CO_FLOW'][:,1]/(4+data['CO_FLOW'][:,1]), 'k-')
##    axis2_array[i].set_ylim(0.01,0.25)
##    
##    axis_array[i].set_xlim(flow_sections[i],flow_sections[i+1])
##    axis_array[i].tick_params(direction='in', length=6, width=2, colors='k',labelsize=14,axis='both',pad=5)
##    axis2_array[i].tick_params(direction='in', length=6, width=2, colors='k',labelsize=14,axis='y',pad=5)
##    
##axis_array[2].set_ylabel('SEM Current / nA', fontsize=20)
##axis2_array[2].set_ylabel('CO/O2 Ratio', fontsize=20)
##axis_array[4].set_xlabel('Time/h', fontsize=20)
##
##
###plt.tight_layout()
##plt.show()
###plt.savefig('../svg_figures/oscillations_gas_dependence.svg')