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
#Silicon
cursor.execute("SELECT x,y FROM xy_values_bifrost where measurement = 3189")
data['si'] = np.array(cursor.fetchall())

#Platinum
cursor.execute("SELECT x,y FROM xy_values_bifrost where measurement = 3188")
data['pt'] =  np.array(cursor.fetchall())

axis_array = []
fig = plt.figure()

for i in range(0,1):
    axis_array.append(fig.add_subplot(1,1,i+1))
    axis_array[i].plot(data['si'][:,0], data['si'][:,1], 'r-')
    axis_array[i].plot(data['pt'][:,0], data['pt'][:,1], 'b-')
    #axis_array[i].set_ylim(0,30)
    axis_array[i].set_xlim(1400,0)
    
    axis_array[i].annotate('Some material', xy=(200, 10000),  xycoords='data', xytext=(260, 35000), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='right', verticalalignment='top',)
    
    axis_array[i].tick_params(direction='in', length=6, width=2, colors='k',labelsize=14,axis='both',pad=5)
    
axis_array[0].set_ylabel('Counts / s', fontsize=20)
axis_array[0].set_xlabel('Binding Energy / eV', fontsize=20)



#plt.tight_layout()
plt.show()
#plt.savefig('../svg_figures/oscillations_gas_dependence.svg')