import matplotlib
from scipy import optimize
import math
#matplotlib.use('svg')
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MySQLdb
import sys
from matplotlib.backends.backend_pdf import PdfPages

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")


cursor = db.cursor()

sys.path.append('tof_figures')
import ammonia_stochiometric_2010_02_15 as config

data = {}

#Get all data from the db
for i in range(0,len(config.temperatures)):
    print config.temperatures[i]
    cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = " + str(i + config.initial_db))
    data[i] = np.array(cursor.fetchall())


treated_data = {}
#Prepare the list that will hold the (temp,intensity) values
for mass in config.masses:
    treated_data[mass[0]] = np.zeros((len(config.temperatures),2))


pp = PdfPages('multipage.pdf')

for j in range(0,len(config.temperatures)):
    pdffig = plt.figure()
    i = 0
    Data = data[j]
    for mass in config.masses:
        i = i + 1
        axis = pdffig.add_subplot(4,3,i)
        center = (int)(mass[1] * 2000) ## Notice... 
        center_mass = mass[1]
        Start = center -40 #Display range
        End = center + 40
        start = center - 8 #Fitting range
        end = center + 8


        x_values = Data[start:end,0]
        y_values = Data[start:end,1]
        #y_values = y_values - min(y_values)
        
        # Fit the first set
        fitfunc = lambda p, x: p[0]*math.e**(-1*((x-center_mass-p[2])**2)/p[1])       # Target function
        errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
        p0 = [50,0.00001,0] # Initial guess for the parameters
        p1, success = optimize.leastsq(errfunc, p0[:], args=(x_values, y_values))        

        if (success > 4) or p1[1]>0.01:
            p0 = [5,0.00001,0]
            p1, success = optimize.leastsq(errfunc, p0[:], args=(x_values[2:5], y_values[2:5]))
       
        if success > 4 or p1[1]>0.01 or p1[1]<0:
            print "p1:" + str(p1[0]) + " p1:" + str(p1[1]) + " p2:" + str(p1[2]) + " j: " + str(j)
            p1[1] = 0

        axis.plot(Data[Start:End,0],Data[Start:End,1],'b-')
        axis.plot([Data[start,0],Data[start,0]],[0,max(y_values)],'k-')
        axis.plot([Data[end,0],Data[end,0]],[0,max(y_values)],'k-')

        axis.plot(Data[Start:End,0],fitfunc(p1, Data[Start:End,0]),'r-')
        axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=8,axis='both',pad=5)
        axis.annotate(mass[0], xy=(.05,.85), xycoords='axes fraction',fontsize=8)
        axis.set_xticks(())
        
        charge = 0
        treated_data[mass[0]][j][0] = config.temperatures[j]
        treated_data[mass[0]][j][1] = math.sqrt(math.pi)*p1[0] * math.sqrt(p1[1])
    plt.savefig(pp, format='pdf')
    plt.close()
pp.close()

colors = ['ro-','bo-','go-','co-','mo-','yo-','r*-','b*-','g*-']
fig = plt.figure()
axis = fig.add_subplot(2,1,1)
fig.subplots_adjust(hspace=0.3)

i = 0
for mass in config.masses:    
    axis.plot(treated_data[mass[0]][:,0],treated_data[mass[0]][:,1], colors[i],label=mass[0])
    i = i + 1
    
    
axis.set_ylabel('Response / mV$\cdot$s', fontsize=14)
axis.set_xlabel('Temperature', fontsize=14)
axis.legend()
axis = fig.add_subplot(2,1,2)
i = 0
for mass in config.masses:    
    axis.plot(treated_data[mass[0]][:,1], colors[i],label=mass[0])
    i = i + 1

axis.set_xlabel('Tentative time', fontsize=14)
axis.set_ylabel('Response / mV$\cdot$s', fontsize=14)

axis2 = axis.twinx()
axis2.plot(treated_data[mass[0]][:,0], 'k.',label='Temperature')
axis2.set_ylabel('Temperature / C', fontsize=14)

axis.legend()

#plt.tight_layout()
plt.show()
#plt.savefig('../svg_figures/oscillations_gas_dependence.svg')
