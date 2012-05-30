backend = 'svg'
execfile('../std_header.py')
import matplotlib.gridspec as gridspec

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")


cursor = db.cursor()

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room) 

ratio = d.ratio
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

gs = gridspec.GridSpec(3, 3)
gs.update(wspace=0.3,hspace=0.25)

#Relevant time, OH: 12.418, NH3: 12.427
data = {}
cursor.execute("SELECT x*1000000,y*1000 FROM xy_values_tof where measurement = 209")
Data = np.array(cursor.fetchall())

masses = []
masses.append(['H$_2$O',12.777,8,'a)'])
masses.append(['H$_2$',4.387,8,'b)'])
masses.append(['O$_2$',16.972,8,'c)'])

x_ticks = []
y_ticks = []
#x_ticks.append([12.767,12.777,12.787])
#x_ticks.append([4.377,4.387,4.397])
#x_ticks.append([16.962,16.972,16.982])
x_ticks.append([12.767,12.787])
x_ticks.append([4.377,4.397])
x_ticks.append([16.962,16.982])
y_ticks.append([0,100,200,300,400])
y_ticks.append([0,5,10,15])
y_ticks.append([0,0.2,0.4,0.6])

fit = []

#X_range = Data[24600:25000,0]
#X_range = np.arange(12.405,12.44,0.0001)

i = 0

for mass in masses:
    i = i + 1
    axis = plt.subplot(gs[:-1, i-1])
    
    center = (int)(mass[1] * 2000) ## Notice... 
    center_mass = mass[1]
    Start = center -35 #Display range
    End = center + 35
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
    signal = math.sqrt(math.pi)*p1[0] * math.sqrt(p1[1])    
    
    axis.plot(X_values,Y_values,'bo',linewidth=1.1,markersize=3)    
    axis.plot(X_values,fitfunc(p1, X_values),'r-',linewidth=1.1)
    axis.ticklabel_format(useOffset=False)
    #axis.set_xlim = (center-10,center+10)

    axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    axis.set_xticks([])
    axis.set_yticks(y_ticks[i-1])
    axis.set_xlim(mass[1]-0.013,mass[1]+0.013)
    #axis.annotate(mass[0], (0.13,0.9),xycoords='axes fraction',fontsize=d.arrowfont)
    axis.annotate(mass[3], (0.13,0.9),xycoords='axes fraction',fontsize=d.arrowfont)
    #axis.annotate(str(round(signal,3)), (0.13,0.8),xycoords='axes fraction',fontsize=d.arrowfont)
    print signal
    if i==1:
        axis.set_ylabel('Response / mV', fontsize=d.y_axis_font)    

    axis = plt.subplot(gs[2, i-1])    
    #Notice! We plot the signal-normalized error function
    axis.plot(X_values,(Y_values-fitfunc(p1, X_values))/signal,'r-',linewidth=1.1)
    axis.ticklabel_format(useOffset=False)
    axis.set_xticks(x_ticks[i-1])
    axis.set_ylim(-20,35)
    axis.set_yticks([-15,0,15,30])
    axis.set_xlim(mass[1]-0.013,mass[1]+0.013)
    if i==1:
        axis.set_ylabel('Norm. Error', fontsize=d.y_axis_font)    
    if i==2:
        axis.set_xlabel('Flight Time / $\mu$s', fontsize=d.x_axis_font)    
    axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
    

#plt.tight_layout()
#plt.show()
plt.savefig('../../svg_figures/dynamic_range.svg')

