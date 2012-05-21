backend = 'svg'
execfile('std_header.py')

##from matplotlib.backends.backend_pdf import PdfPages

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")


cursor = db.cursor()

sys.path.append('tof')
import combined_tof_and_qms as config

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room*0.95) 
fig.subplots_adjust(hspace=0.1)

ratio = 1
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

data = {}

#Get all data from the db
for i in range(0,len(config.temperatures)):
    print config.temperatures[i]
    cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = " + str(i + config.initial_db))
    data[i] = np.array(cursor.fetchall())


treated_data = {}
#Prepare the list that will hold the (temp,intensity) values
for mass in config.masses:
    treated_data[mass[0]] = np.zeros((len(config.temperatures),3))


##pp = PdfPages('multipage.pdf')
for j in range(0,len(config.temperatures)):
    print j
    ##pdffig = plt.figure()
    i = 0
    Data = data[j]
    for mass in config.masses:
        i = i + 1
        ##axis = pdffig.add_subplot(4,3,i)
        center = (int)(mass[1] * 2000) ## Notice... 
        center_mass = mass[1]
        Start = center -40 #Display range
        End = center + 40
        start = center - mass[2] #Fitting range
        end = center + mass[2]

        offset = min(Data[Start:End,1])
        x_values = Data[start:end,0]
        y_values = Data[start:end,1]-offset
        X_values = Data[Start:End,0]
        Y_values = Data[Start:End,1]-offset
        
        # Fit the first set
        fitfunc = lambda p, x: p[0]*math.e**(-1*((x-center_mass-p[2])**2)/p[1])       # Target function
        errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
        p0 = [50,0.00001,0] # Initial guess for the parameters
        p1, success = optimize.leastsq(errfunc, p0[:], args=(x_values, y_values),maxfev=1000)        

        if (success > 4) or p1[1]>0.01:
            p0 = [5,0.00001,0]
            p1, success = optimize.leastsq(errfunc, p0[:], args=(x_values[2:5], y_values[2:5]))
       
        if success > 4 or p1[1]>0.01 or p1[1]<0:
            print "p1:" + str(p1[0]) + " p1:" + str(p1[1]) + " p2:" + str(p1[2]) + " j: " + str(j)
            p1[1] = 0

        ##axis.plot(X_values,Y_values,'b-')
        ##axis.plot([Data[start,0],Data[start,0]],[0,max(y_values)],'k-')
        ##axis.plot([Data[end,0],Data[end,0]],[0,max(y_values)],'k-')

        ##axis.plot(X_values,fitfunc(p1, X_values),'r-')
        ##axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=8,axis='both',pad=5)
        ##axis.annotate(mass[0], xy=(.05,.85), xycoords='axes fraction',fontsize=8)
        ##axis.set_xticks(())
        
        charge = 0
        treated_data[mass[0]][j][0] = config.temperatures[j]
        treated_data[mass[0]][j][1] = math.sqrt(math.pi)*p1[0] * math.sqrt(p1[1])
        treated_data[mass[0]][j][2] = config.times[j]
    ##plt.savefig(pp, format='pdf')
    ##plt.close()
##pp.close()

colors = ['ro-','go-','co-','ko-','r*-','b*-','g*-']
axis = fig.add_subplot(2,1,1)


"""
i = 0
for mass in config.masses:    
    axis.plot(treated_data[mass[0]][:,0],treated_data[mass[0]][:,1], colors[i],label=mass[0])
    i = i + 1
    
    
axis.set_ylabel('Response / mV$\cdot$s', fontsize=14)
axis.set_xlabel('Temperature', fontsize=14)
axis.legend()

"""


axis = fig.add_subplot(2,1,1)
#t0 = config.times[0]
t0 =  1336071574#Timestamp of corresponding QMS measurement
i = 0
for mass in config.masses:
    axis.plot((treated_data[mass[0]][:,2]-t0)/60,treated_data[mass[0]][:,1]*1000, colors[i],label=mass[0],markersize=0.75)
    #axis.plot(treated_data[mass[0]][:,1], colors[i],label=mass[0])
    i = i + 1

#axis.set_xlabel('Time / minutes', fontsize=d.x_axis_font)
axis.set_ylabel('Response / mV$\cdot \mu$s', fontsize=d.y_axis_font)
axis.set_xlim(140,320)

axis2 = axis.twinx()
#axis2.plot(treated_data[mass[0]][:,0], 'k.',label='Temperature')
axis2.plot((treated_data[mass[0]][:,2]-t0)/60,treated_data[mass[0]][:,0], 'bo-',label='Temperature',markersize=0.75)
axis2.set_ylabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)
axis.set_xticklabels([])
axis2.set_xticklabels([])
axis2.set_yticks((50,100,150,200,250))
axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis2.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

axis2.set_xlim(140,320)
axis.set_ylim(0,500)
axis2.set_ylim(0,300)

arrow = dict(facecolor='black',arrowstyle='->')
axis.annotate('NH$_3$', xy=(175, 302),  xycoords='data', xytext=(170, 368), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('H$_2$O', xy=(195, 410),  xycoords='data', xytext=(180, 440), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('N$_2$', xy=(250, 210),  xycoords='data', xytext=(245, 140), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('N$_2$O', xy=(170, 200),  xycoords='data', xytext=(158, 245), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('Temp', xy=(270, 250),  xycoords='data', xytext=(290, 410), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)



axis = fig.add_subplot(2,1,2)

data = {}
#M17
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 2149")
data['M17'] = np.array(cursor.fetchall())
#18
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 2151")
data['M18'] =  np.array(cursor.fetchall())
#M28
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 2152")
data['M28'] =  np.array(cursor.fetchall())
#M30
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 2154")
data['M30'] =  np.array(cursor.fetchall())
#M32
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 2150")
data['M32'] =  np.array(cursor.fetchall())
#M44
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 2153")
data['M44'] =  np.array(cursor.fetchall())
#M46
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = 2155")
data['M46'] =  np.array(cursor.fetchall())
#Temperature
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 2160")
data['TEMPERATURE'] =  np.array(cursor.fetchall())

axis.plot(data['M17'][:,0], data['M17'][:,1], 'r-')
axis.plot(data['M18'][:,0], data['M18'][:,1], 'g-')
axis.plot(data['M28'][:,0], data['M28'][:,1], 'c-')
#axis.plot(data['M32'][:,0], data['M32'][:,1], 'm-')
axis.plot(data['M44'][:,0], data['M44'][:,1], 'k-')
axis.set_xlim(140,320)
axis.set_ylim(0,8)
axis2.set_ylim(0,300)
axis.set_ylabel('SEM current / nA', fontsize=d.y_axis_font)
axis.set_xlabel('Time / minutes', fontsize=d.x_axis_font)

axis2 = axis.twinx()
axis2.plot(data['TEMPERATURE'][:,0], data['TEMPERATURE'][:,1], 'b-')
axis2.set_ylabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)
#axis2.set_yticks((50,150,250))
axis2.set_xlim(140,320)
axis2.set_yticks((50,100,150,200,250))

arrow = dict(facecolor='black',arrowstyle='->')
axis.annotate('NH$_3$', xy=(160, 6),  xycoords='data', xytext=(190, 7), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('H$_2$O', xy=(218, 5),  xycoords='data', xytext=(240, 6), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('N$_2$', xy=(267, 0.6),  xycoords='data', xytext=(280, 3), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('N$_2$O', xy=(200, 0.8),  xycoords='data', xytext=(180, 1.8), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)
axis.annotate('Temp', xy=(235, 6.8),  xycoords='data', xytext=(270, 7.2), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=d.arrowfont,)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis2.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

#plt.tight_layout()
#plt.show()
plt.savefig('../svg_figures/tof_combined_tof_and_qms.svg')
