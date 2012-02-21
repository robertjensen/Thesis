import sys
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


sys.path.append('area_measurements')
#import MR102_approx20cov_5_2nm as config
#import MR102_approx20cov_5_2nm_II as config
import MR108_40cov_5_0nm as config


data = {}
cursor.execute(config.M44)
data['M44'] = np.array(cursor.fetchall())
cursor.execute(config.CO_FLOW)
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

for i in config.skip:
    del titrations[i]
print len(titrations)


i = 0
for row in titrations:
    while data['M44'][i,0] <row:
        i = i+1
    times.append(i)


axis_array = []
fig = plt.figure()

print len(times)

for i in range(0,len(times)):
    axis_array.append(fig.add_subplot(config.layout_x,config.layout_y,i+1))
    start = times[i]+config.start
    end = times[i]+config.end
    mean_y = [sum(data['M44'][start:start+20,1])/20,sum(data['M44'][end-20:end,1])/20]
    mean_x = [data['M44'][start+20,0],data['M44'][end-20,0]]
    axis_array[i].plot(data['M44'][start:end,0], data['M44'][start:end,1], 'r-')
    axis_array[i].plot(mean_x, mean_y, 'b-')
    axis_array[i].set_ylim(0,0.2)
    
    #axis_array[i].plot(data['M44'][start+650:end+600,0]-4300, data['M44'][start+650:end+600,1], 'g-')    
    
    #axis_array[i].set_xlim(data['M44'][start,0],data['M44'][end,0])
    
    f2 = interp1d([start,end], mean_y)
    charge = 0
    for j in range(start,end):
        charge = charge + (data['M44'][j,1]-f2(j))*(data['M44'][j,0]-data['M44'][j-1,0])
    print charge
    
    axis_array[i].text(0.15, 0.8,round(charge,2),horizontalalignment='center',verticalalignment='center',transform = axis_array[i].transAxes,fontsize=10)
    
    #axis_array[i].tick_params(direction='in', length=6, width=2, colors='k',labelsize=6,axis='both',pad=5)
    axis_array[i].tick_params(direction='in', length=3, width=1, colors='k',labelsize=0,axis='both',pad=5)
    
#axis_array[0].set_ylabel('Ion Current / nA', fontsize=20)
#axis_array[0].set_xlabel('Time / s', fontsize=20)



#plt.tight_layout()
plt.show()
#plt.savefig('../svg_figures/oscillations_gas_dependence.svg')
#plt.savefig('area_multiple_treatments.png',dpi=300)