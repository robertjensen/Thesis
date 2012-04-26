backend = 'svg'
execfile('std_header.py')

def average(values):
    """Computes the arithmetic mean of a list of numbers.

    >>> print average([20, 30, 70])
    40.0
    """
    return sum(values, 0.0) / len(values)


data = {}
#Mass28
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactor where measurement = 6133")
data['M28'] = np.array(cursor.fetchall())

#Mass44
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactor where measurement = 6135")
data['M44'] =  np.array(cursor.fetchall())

#Limit: everytime M44 goes above 4.5nA we start a new oscillation
i = 0
old_m44 = 0
mass_indexes = []
oscillations = [] #Holds the switching times
for row in data['M44']:
    i = i+1
    if (row[1] > (4.5)) and (old_m44<4.5):
        oscillations.append(row[0])
        old_m44 = row[1]
        mass_indexes.append(i)
        
    if (i%10==0):
        old_m44 = row[1]
    
    
periods = []
periods.append(0)
m44_average = []
m44_average.append(0)
m28_average = []
m28_average.append(0)
eff = []
eff.append(0)
for i in range(1,len(oscillations)):
    periods.append(oscillations[i]-oscillations[i-1])
    
    m44_av = average(data['M44'][mass_indexes[i-i]:mass_indexes[i],1])
    m44_average.append(m44_av)
    m28_av = average(data['M28'][mass_indexes[i-i]:mass_indexes[i],1])
    m28_average.append(m28_av)
    eff.append(m44_av/m28_av)

#print len(periods)

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
axis.plot(oscillations, m28_average, 'r.',markersize=0.5)
axis.plot(oscillations, m44_average, 'g.',markersize=0.5)
axis.plot(oscillations, eff, 'k.',markersize=0.5)
#axis.plot(data['M28'][:,0], data['M28'][:,1], 'r-')
#axis.plot(data['M44'][:,0], data['M44'][:,1], 'b-')

arrow = dict(facecolor='black',arrowstyle='->')
axis.annotate('CO$_2$', xy=(2500, 3.4),  xycoords='data', xytext=(2100, 3.1), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('CO', xy=(2500, 2.1),  xycoords='data', xytext=(2100, 2.4), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('CO$_2$/CO', xy=(2500, 1.6),  xycoords='data', xytext=(2100, 1.3), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)


axis.set_ylim(1,4)
axis.set_xlim(700,6000)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis.grid(False)    

axis.set_ylabel('Integrated charge (a.u.)', fontsize=d.y_axis_font)
axis.set_xlabel('Time / min', fontsize=d.y_axis_font)

#plt.tight_layout()
#plt.show()
plt.savefig('../svg_figures/oscil_dutycycle.svg')
