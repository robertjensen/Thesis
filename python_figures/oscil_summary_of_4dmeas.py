backend = 'svg'
execfile('std_header.py')

data = {}
#Mass28
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactor where measurement = 6133")
data['M28'] = np.array(cursor.fetchall())

#Mass44
cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactor where measurement = 6135")
data['M44'] =  np.array(cursor.fetchall())

#Limit: everytime M44 goes above 4.5nA we start a new oscillation
i = 0
old_m44 = 0
oscillations = [] #Holds the switching times
for row in data['M44']:
    i = i+1
    if (row[1] > (4.5)) and (old_m44<4.5):
        oscillations.append(row[0])
        old_m44 = row[1]
        
    if (i%10==0):
        old_m44 = row[1]
    

    
periods = []
periods.append(0)
for i in range(1,len(oscillations)):
    periods.append(oscillations[i]-oscillations[i-1])

#print len(periods)

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room) 

ratio = d.ratio
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)


axis = fig.add_subplot(1,1,1)
axis.plot(oscillations, periods, 'b.')
#axis.plot([750,6000],[1.8,17],'r-')
#axis.plot([750,5000],[5,43],'r-')
range = np.arange(700,6500)

fitfunc = lambda p, x: p[0]*(x**p[1])+p[2]       # Target function
errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
p0 = [0.2,0.6,2] # Initial guess for the parameters
p1, success = optimize.leastsq(errfunc, p0[:], args=([700,1000,2000,4000,6000],[4,6,20,37,45]),maxfev=1000)
print p1, success
axis.plot(range,p1[0]*(range**(p1[1]))+p1[2],'r-')

p1, success = optimize.leastsq(errfunc, p0[:], args=([500,1000,2000,4000,6000],[0,2,9,11,16]),maxfev=1000)
print p1, success
axis.plot(range,p1[0]*(range**(p1[1]))+p1[2],'r-')
#axis.plot(data['M28'][:,0], data['M28'][:,1], 'r-')
#axis.plot(data['M44'][:,0], data['M44'][:,1], 'b-')
#axis.set_ylim(0,7)
#axis.set_xlim(0,500)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis.grid(False)    

axis.set_ylabel('Oscil. period / minutes', fontsize=d.y_axis_font)
axis.set_xlabel('Time / min', fontsize=d.x_axis_font)

a = plt.axes([.18, .65, .3, .15], axisbg='w')
a.plot(oscillations, periods, 'b,')
a.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
plt.setp(a, xlim=(700,1500), ylim=(2,8),xticks=[900,1100,1300], yticks=[3,5,7])

#plt.tight_layout()
#plt.show()
plt.savefig('../svg_figures/oscil_summary_of_4dmeas.svg')
