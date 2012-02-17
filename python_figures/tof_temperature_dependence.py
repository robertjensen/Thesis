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


temperatures = [40,60,80,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,185,190,180,175,170,165,160,155,150,145,140,135,130,125,120,115,110,105,100]
initial_db = 189

masses = [12.43,12.77]

data = {}

for i in range(0,len(temperatures)):
    print temperatures[i]
    cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = " + str(i + initial_db))
    data[i] = np.array(cursor.fetchall())


treated_data = {}
for j in range(0,len(masses)):
    treated_data[str(masses[j])] = np.zeros((len(temperatures),2))


for i in range(0,len(masses)):
    start = (int)((masses[i] * 2000) -50)
    end = (int)((masses[i] * 2000) + 50)
    for j in range(0,len(temperatures)):
        charge = 0
        for k in range(start,end):
            charge = charge + data[j][k,1]
        treated_data[str(masses[i])][j][0] = temperatures[j]
        treated_data[str(masses[i])][j][1] = charge


fig = plt.figure()
axis_array = []

colors = ['ro-','bo-','go-']
axis_array.append(fig.add_subplot(1,1,1))
i = 0
for mass in masses:    
    axis_array[0].plot(treated_data[str(mass)][:,0],treated_data[str(mass)][:,1], colors[i])
    i = i + 1
    
    
axis_array[0].set_ylabel('Intensity', fontsize=20)
axis_array[0].set_xlabel('Temperature', fontsize=20)



#plt.tight_layout()
plt.show()
#plt.savefig('../svg_figures/oscillations_gas_dependence.svg')

