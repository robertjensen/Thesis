backend = 'svg'
execfile('std_header.py')

import datetime

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room*0.95) 

ratio = 0.7
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

data = {}
#Rouging pressure
cursor.execute("SELECT unix_timestamp(time),pressure FROM pressure_microreactor where time between \"2012-04-15 00:00\" and \"2012-05-24 12:39\" order by time")
data['pressure'] = np.array(cursor.fetchall())
#Turbo temp.
cursor.execute("SELECT unix_timestamp(time), temperature FROM temperature_microreactor_chamberturbo where temperature between -1 and 1300 and time between \"2012-04-15 00:00\" and \"2012-05-24 12:38\" order by time")
data['temp'] =  np.array(cursor.fetchall())

"""
t = data['pressure']
print t(0,0)
a = data['pressure'][0:5,0]
print a
b = datetime.date.fromtimestamp(a)
print b
"""

axis = fig.add_subplot(2,1,1)
t0 = data['pressure'][0,0]
axis.plot((data['pressure'][:,0]-t0)/(24*60*60), data['pressure'][:,1], 'b-')
axis.set_yscale('log')
axis.set_ylim(1e-9,1e-5)
#axis2 = axis.twinx()
axis.set_xticklabels([])

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis.set_ylabel('Pressure / mbar', fontsize=d.y_axis_font)
#axis.set_xlabel('Time / days', fontsize=d.x_axis_font)

axis = fig.add_subplot(2,1,2)
t0 = data['temp'][0,0]
axis.plot((data['temp'][:,0]-t0)/(24*60*60), data['temp'][:,1], 'b-')
#axis.set_yscale('log')
#axis.set_ylim(0,0.5)
#axis2 = axis.twinx()

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis.set_ylabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)
axis.set_xlabel('Time / days', fontsize=d.x_axis_font)


#plt.tight_layout()
plt.show()
plt.savefig('../svg_figures/db_examples.svg')
