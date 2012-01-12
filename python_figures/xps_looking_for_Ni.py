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
    axis_array[i].set_xlim(1100,0)
    
    axis_array[i].annotate('O KLL', xy=(975, 18000),  xycoords='data', xytext=(900, 32000), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='right', verticalalignment='top',)
    axis_array[i].annotate('Ni 2p', xy=(860, 17000),  xycoords='data', xytext=(860, 38000), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='right', verticalalignment='top',)
    axis_array[i].annotate('O 1s', xy=(530, 18000),  xycoords='data', xytext=(590, 25000), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='right', verticalalignment='top',)
    axis_array[i].annotate('Pt 4p3/2', xy=(521, 16000),  xycoords='data', xytext=(450, 30000), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='right', verticalalignment='top',)    
    axis_array[i].annotate('Ti 2p', xy=(460, 16000),  xycoords='data', xytext=(380, 21000), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='right', verticalalignment='top',)
    axis_array[i].annotate('Pt 4d', xy=(322, 14000),  xycoords='data', xytext=(322, 30000), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='right', verticalalignment='top',)        
    axis_array[i].annotate('Pt 4f', xy=(70, 18000),  xycoords='data', xytext=(60, 35000), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='right', verticalalignment='top',)
    axis_array[i].annotate('Si 2p', xy=(105, 11000),  xycoords='data', xytext=(130, 20000), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='right', verticalalignment='top',)
    axis_array[i].annotate('Si 2s', xy=(152, 9000),  xycoords='data', xytext=(190, 12000), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='right', verticalalignment='top',)
    axis_array[i].annotate('C 1s', xy=(286, 26000),  xycoords='data', xytext=(260, 32000), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='right', verticalalignment='top',)    
    axis_array[i].annotate('O 2s', xy=(28, 2000),  xycoords='data', xytext=(26, 15000), textcoords='data', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='right', verticalalignment='top',)    
    
    axis_array[i].tick_params(direction='in', length=6, width=2, colors='k',labelsize=14,axis='both',pad=5)
    
axis_array[0].set_ylabel('Counts / s', fontsize=20)
axis_array[0].set_xlabel('Binding Energy / eV', fontsize=20)



#plt.tight_layout()
plt.show()
#plt.savefig('../svg_figures/oscillations_gas_dependence.svg')