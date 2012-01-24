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
#Cyclohexane
cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = 173")
data['ch'] = np.array(cursor.fetchall())


n = 2
smooth_data = data['ch']
smooth = []
for i in range(0,len(smooth_data)/n):
    #print i
    start = i*n
    end = (i*n)+n
    x_average = sum(smooth_data[start:end,0])/n
    y_average = sum(smooth_data[start:end,1])/n
    smooth.append([x_average,y_average])
  
data['ch'] = np.array(smooth)

#Background
cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = 172")
data['bg'] =  np.array(cursor.fetchall())

axis_array = []
fig = plt.figure()

for i in range(0,1):
    axis_array.append(fig.add_subplot(1,1,i+1))
    axis_array[i].plot(data['ch'][:,0], data['ch'][:,1], 'r-')
    axis_array[i].plot(data['bg'][:,0], data['bg'][:,1], 'b-')
    axis_array[i].set_ylim(0,100)
    axis_array[i].set_xlim(0,50)
    
    
    
    axis_array[i].tick_params(direction='in', length=6, width=2, colors='k',labelsize=14,axis='both',pad=5)
    
axis_array[0].set_ylabel('Response / mV', fontsize=20)
axis_array[0].set_xlabel('Flight Time / $\mu$s', fontsize=20)



#plt.tight_layout()
plt.show()
#plt.savefig('../svg_figures/oscillations_gas_dependence.svg')