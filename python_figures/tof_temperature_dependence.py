import matplotlib
#matplotlib.use('svg')
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MySQLdb
import sys

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")


cursor = db.cursor()

sys.path.append('tof_figures')
import ammonia_stochiometric_2010_02_15 as config

data = {}

for i in range(0,len(config.temperatures)):
    print config.temperatures[i]
    cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = " + str(i + config.initial_db))
    data[i] = np.array(cursor.fetchall())


treated_data = {}
for j in range(0,len(config.masses)):
    treated_data[str(config.masses[j][1])] = np.zeros((len(config.temperatures),2))


for i in range(0,len(config.masses)):
    start = (int)((config.masses[i][1] * 2000) -5)
    end = (int)((config.masses[i][1] * 2000) + 5)
    for j in range(0,len(config.temperatures)):
        charge = 0
        for k in range(start,end):
            charge = charge + data[j][k,1]
        treated_data[str(config.masses[i][1])][j][0] = config.temperatures[j]
        treated_data[str(config.masses[i][1])][j][1] = charge


fig = plt.figure()

colors = ['ro-','bo-','go-']
axis = fig.add_subplot(2,1,1)

i = 0
for mass in config.masses:    
    axis.plot(treated_data[str(mass[1])][:,0],treated_data[str(mass[1])][:,1], colors[i],label=str(mass[0]))
    i = i + 1
    
    
axis.set_ylabel('Intensity', fontsize=20)
axis.set_xlabel('Temperature', fontsize=20)
axis.legend()
axis = fig.add_subplot(2,1,2)
i = 0
for mass in config.masses:    
    axis.plot(treated_data[str(mass[1])][:,1], colors[i],label=str(mass[0]))
    i = i + 1

axis.set_xlabel('Tentitative time', fontsize=20)
axis.set_ylabel('Intensity', fontsize=20)

axis2 = axis.twinx()
axis2.plot(treated_data[str(mass[1])][:,0], 'k.',label='Temperature')
axis2.set_ylabel('Temperature / C', fontsize=20)

axis.legend()

#plt.tight_layout()
plt.show()
#plt.savefig('../svg_figures/oscillations_gas_dependence.svg')

