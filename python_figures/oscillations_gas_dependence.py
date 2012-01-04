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
#Mass28
cursor.execute("SELECT x/3600000,y FROM xy_values_microreactor where measurement = 6694")
data['M28'] = np.array(cursor.fetchall())

#Mass44
cursor.execute("SELECT x/3600000,y FROM xy_values_microreactor where measurement = 6696")
data['M44'] =  np.array(cursor.fetchall())

#CO Flow
cursor.execute("SELECT x/3600000,y FROM xy_values_microreactor where measurement = 6702")
data['CO_FLOW'] = np.array(cursor.fetchall())


fig = plt.figure()
axis_array = []
axis2_array = []

for i in range(0,5):
    axis_array.append(fig.add_subplot(5,1,i+1))
    axis_array[i].plot(data['M28'][:,0], data['M28'][:,1]*1e9, 'r-')
    axis_array[i].plot(data['M44'][:,0], data['M44'][:,1]*1e9, 'b-')
    axis_array[i].set_ylim(0,1.85)
    axis2_array.append(axis_array[i].twinx())
    axis2_array[i].plot(data['CO_FLOW'][:,0], data['CO_FLOW'][:,1]/(4+data['CO_FLOW'][:,1]), 'k-')
    axis2_array[i].set_ylim(0.01,0.25)
    
    axis_array[i].set_xlim(i*15+0.9,(i+1)*15+1)
    axis_array[i].tick_params(direction='in', length=6, width=2, colors='k',labelsize=14,axis='both',pad=5)
    axis2_array[i].tick_params(direction='in', length=6, width=2, colors='k',labelsize=14,axis='y',pad=5)
    
axis_array[2].set_ylabel('SEM Current / nA', fontsize=20)
axis2_array[2].set_ylabel('CO/O2 Ratio', fontsize=20)
axis_array[4].set_xlabel('Time/h', fontsize=20)



#plt.tight_layout()
plt.show()
#plt.savefig('../svg_figures/oscillations_gas_dependence.svg')