import matplotlib
matplotlib.use('svg')
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MySQLdb

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    print "Dav"


cursor = db.cursor()

data = {}
#Mass28
cursor.execute("SELECT x/1000,y FROM xy_values_microreactor where measurement = 6694")
data['M28'] = np.array(cursor.fetchall())

#Mass44
cursor.execute("SELECT x/1000,y FROM xy_values_microreactor where measurement = 6696")
data['M44'] =  np.array(cursor.fetchall())
#CO Flow
cursor.execute("SELECT x/1000,y FROM xy_values_microreactor where measurement = 6702")
data['CO_FLOW'] = np.array(cursor.fetchall())


plt.plot(data['M28'][:,0], data['M28'][:,1], 'r--')
#plt.savefig('./scratch/test.png',bbox_inches='tight')
#plt.tight_layout()
plt.savefig('./scratch/test.svg')