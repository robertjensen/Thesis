import matplotlib
#matplotlib.use('svg')
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MySQLdb

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")


cursor = db.cursor()

data = {}
#Ambient
cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = 117")
data['ambient'] = np.array(cursor.fetchall())

#200C
cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = 115")
data['hot'] =  np.array(cursor.fetchall())



fig = plt.figure()
axis_array = []
x_ranges = []
x_ranges.append((17,33))
x_ranges.append((15,33))
x_ranges.append((26,33))

y_ranges = []
y_ranges.append((0,30))
y_ranges.append((0,30))
y_ranges.append((0,15))


for i in range(0,1):
    axis_array.append(fig.add_subplot(1,1,i+1))
    mass_values = ((data['hot'][:,0]-0.095) / 2.96373200801)**2.01054 
    axis_array[i].plot(mass_values, data['hot'][:,1], 'r-')
    
    mass_values = ((data['ambient'][:,0]-0.095) / 2.96373200801)**2.01054
    axis_array[i].plot(mass_values, data['ambient'][:,1], 'b-')
    axis_array[i].set_ylim(y_ranges[i])
    
    axis_array[i].set_xlim(x_ranges[i])
    axis_array[i].tick_params(direction='in', length=6, width=2, colors='k',labelsize=14,axis='both',pad=5)
    
axis_array[0].set_ylabel('MCP Response / mV', fontsize=20)
axis_array[0].set_xlabel('Mass / AMU', fontsize=20)



#plt.tight_layout()
plt.show()
#plt.savefig('../svg_figures/oscillations_gas_dependence.svg')