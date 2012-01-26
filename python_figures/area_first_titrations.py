import matplotlib
#matplotlib.use('svg')
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MySQLdb
from scipy.interpolate import interp1d

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")


cursor = db.cursor()

data = {}
#M44
cursor.execute("SELECT x/1000,y*1e9 FROM xy_values_microreactor where measurement = 6874")
data['M44'] = np.array(cursor.fetchall())

#CO Flow
cursor.execute("SELECT x/1000,y FROM xy_values_microreactor where measurement = 6880")
data['CO_FLOW'] =  np.array(cursor.fetchall())

i = 0
old_m44 = 0
titrations = [] #Holds the switching times
times = []
for row in data['CO_FLOW']:
    i = i+1
    if (row[1] > (0.5)) and (old_m44<0.5):
        titrations.append(row[0])
        old_m44 = row[1]
        
    if (i%10==0):
        old_m44 = row[1]

i = 0
for row in titrations:
    while data['M44'][i,0] <row:
        i = i+1
    times.append(i)


axis_array = []
fig = plt.figure()

for i in range(0,len(times)):
    axis_array.append(fig.add_subplot(3,2,i+1))
    start = times[i]+90
    end = times[i]+210
    mean_y = [sum(data['M44'][start:start+10,1])/10,sum(data['M44'][end-10:end,1])/10]
    mean_x = [data['M44'][start+10,0],data['M44'][end-10,0]]
    axis_array[i].plot(data['M44'][start:end,0], data['M44'][start:end,1], 'r-')
    axis_array[i].plot(mean_x, mean_y, 'b-')
    axis_array[i].set_ylim(0,0.12)
    #axis_array[i].set_xlim(0,50)
    
    f2 = interp1d([start,end], mean_y)
    charge = 0
    for j in range(start,end):
        charge = charge + data['M44'][j,1]*(data['M44'][j,0]-data['M44'][j-1,0]) - f2(j)
    print charge
    
    axis_array[i].text(0.15, 0.8,round(charge,2),horizontalalignment='center',verticalalignment='center',transform = axis_array[i].transAxes,fontsize=16)
    
    axis_array[i].tick_params(direction='in', length=6, width=2, colors='k',labelsize=14,axis='both',pad=5)
    
axis_array[0].set_ylabel('Ion Current / nA', fontsize=20)
axis_array[0].set_xlabel('Time / s', fontsize=20)



#plt.tight_layout()
plt.show()
#plt.savefig('../svg_figures/oscillations_gas_dependence.svg')