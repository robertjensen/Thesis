import matplotlib
matplotlib.use('svg')
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
#cursor.execute("SELECT x/1000,y FROM xy_values_microreactor where measurement = 6702")
#data['CO_FLOW'] = np.array(cursor.fetchall())


for i in range(0,6):
    plt.subplot(6,1,i+1)
    plt.plot(data['M28'][:,0], data['M28'][:,1], 'r--')
    plt.plot(data['M44'][:,0], data['M44'][:,1], 'b--')
    #plt.xlim((i*14400)+2000,(((i+1)*14400)+3000))
    plt.xlim(i*12+1,(i+1)*12+1)
    plt.ylim(0,1.5e-9)
    plt.yticks(arange(6),fontsize=20)



#plt.tight_layout()
plt.show()
plt.savefig('../svg_figures/oscillations_gas_dependence.svg')