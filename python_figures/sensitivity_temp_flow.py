backend = 'svg'
execfile('std_header.py')

data = {}

#Chamber pressure, N5
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 498 and x between 6500000 and 15850000")
data['P5'] =  np.array(cursor.fetchall())
#Temperature,N5
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 502 and x between 6500000 and 15850000")
data['T5'] =  np.array(cursor.fetchall())

#Chamber pressure, N8
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 459 and x between 9200000 and 16400000")
data['P8'] =  np.array(cursor.fetchall())
#Temperature,N8
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 463 and x between 9200000 and 16400000")
data['T8'] =  np.array(cursor.fetchall())

#Chamber pressure, N9
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 446 and x between 5850000 and 12100000")
data['P9'] =  np.array(cursor.fetchall())
#Temperature,N9
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 450 and x between 5850000 and 12100000")
data['T9'] =  np.array(cursor.fetchall())

#Chamber pressure, N10
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 314 and x between 6000000 and 12000000")
data['P10'] =  np.array(cursor.fetchall())
#Temperature,N10
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 318 and x between 6000000 and 12000000")
data['T10'] =  np.array(cursor.fetchall())

#Chamber pressure, N11
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 343 and x between 6800000 and 12500000")
data['P11'] =  np.array(cursor.fetchall())
#Temperature,N11
cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = 347 and x between 6800000 and 12500000")
data['T11'] =  np.array(cursor.fetchall())


temp5_interp = interpolate.interp1d(data['T5'][:,0],data['T5'][:,1]+273.15, bounds_error=False)
temp8_interp = interpolate.interp1d(data['T8'][:,0],data['T8'][:,1]+273.15, bounds_error=False)
temp9_interp = interpolate.interp1d(data['T9'][:,0],data['T9'][:,1]+273.15, bounds_error=False)
temp10_interp = interpolate.interp1d(data['T10'][:,0],data['T10'][:,1]+273.15, bounds_error=False)
temp11_interp = interpolate.interp1d(data['T11'][:,0],data['T11'][:,1]+273.15, bounds_error=False)

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room) 

ratio = 1
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

gs = gridspec.GridSpec(4, 1)
axis = plt.subplot(gs[0:2, 0])

fitfunc = lambda p, x: p[0]/(p[1]+x)       # Target function
errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
p0 = [2e-4,0] # Initial guess for the parameters

p1, success = optimize.leastsq(errfunc, p0[:], args=(temp8_interp(data['P8'][2:250,0]),data['P8'][2:250,1]),maxfev=1000)
axis.plot(temp8_interp(data['P8'][:,0]), data['P8'][:,1], 'b-')
axis.plot(temp8_interp(data['P8'][2:250,0]), fitfunc(p1,temp8_interp(data['P8'][2:250,0])),'b--')

p1, success = optimize.leastsq(errfunc, p0[:], args=(temp11_interp(data['P11'][15:250,0]),data['P11'][15:250,1]),maxfev=1000)
axis.plot(temp11_interp(data['P11'][:,0]), data['P11'][:,1], 'c-')
axis.plot(temp11_interp(data['P11'][5:310,0]), fitfunc(p1,temp11_interp(data['P11'][5:310,0])),'c--')
axis.set_xlim(250,700)
#axis.set_ylim(0,0.5)
#axis.set_yscale('log')

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis.set_xticklabels([])
#axis.set_yticklabels([1.0e-7,1.5e-7,2e-7])
#axis.set_ylabel('Pressure / mbar', fontsize=d.y_axis_font)
#axis2.set_ylabel('Chamber pressure / mbar', fontsize=d.y_axis_font)
#axis.set_xticklabels([])

#arrow = dict(facecolor='black',arrowstyle='->')
#font = d.arrowfont
#axis.annotate('CO$_2$', xy=(345, 7e-9),  xycoords='data', xytext=(300, 9e-9), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
#axis.annotate('Pressure', xy=(80, 7e-9),  xycoords='data', xytext=(90, 5.3e-9), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)

axis = plt.subplot(gs[2, 0])
axis.plot(temp5_interp(data['P5'][:,0]), data['P5'][:,1]*1e7, 'r-')
axis.plot(temp8_interp(data['P8'][:,0]), data['P8'][:,1]*1e7, 'b-')
axis.plot(temp9_interp(data['P9'][:,0]), data['P9'][:,1]*1e7, 'g-')
axis.plot(temp10_interp(data['P10'][:,0]), data['P10'][:,1]*1e7, 'k-')
axis.plot(temp11_interp(data['P11'][:,0]), data['P11'][:,1]*1e7, 'c-')
axis.set_ylabel('Pressure / mbar', fontsize=d.y_axis_font)
axis.set_xlim(250,700)
axis.set_yticks([1,1.5,2])
axis.set_xticks([])
axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

axis = plt.subplot(gs[3, 0])
p0 = [2e-4,0] # Initial guess for the parameters
p1, success = optimize.leastsq(errfunc, p0[:], args=(temp5_interp(data['P5'][50:750,0]),data['P5'][50:750,1]),maxfev=1000)
axis.plot(temp5_interp(data['P5'][50:750,0]), 1e7*fitfunc(p1,temp5_interp(data['P5'][50:750,0])),'r--')

p1, success = optimize.leastsq(errfunc, p0[:], args=(temp8_interp(data['P8'][2:250,0]),data['P8'][2:250,1]),maxfev=1000)
axis.plot(temp8_interp(data['P8'][2:250,0]), 1e7*fitfunc(p1,temp8_interp(data['P8'][2:250,0])),'b--')

p1, success = optimize.leastsq(errfunc, p0[:], args=(temp9_interp(data['P9'][2:230,0]),data['P9'][2:230,1]),maxfev=1000)
axis.plot(temp9_interp(data['P9'][2:230,0]), 1e7*fitfunc(p1,temp9_interp(data['P9'][2:230,0])),'g--')

p1, success = optimize.leastsq(errfunc, p0[:], args=(temp10_interp(data['P10'][2:330,0]),data['P10'][2:330,1]),maxfev=1000)
axis.plot(temp10_interp(data['P10'][2:330,0]), 1e7*fitfunc(p1,temp10_interp(data['P10'][2:330,0])),'k--')

p1, success = optimize.leastsq(errfunc, p0[:], args=(temp11_interp(data['P11'][15:250,0]),data['P11'][15:250,1]),maxfev=1000)
axis.plot(temp11_interp(data['P11'][15:250,0]), 1e7*fitfunc(p1,temp11_interp(data['P11'][15:250,0])),'c--')
axis.set_xlim(250,700)
axis.set_yticks([1,1.5,2])
axis.set_xlabel('Temperature / K', fontsize=d.y_axis_font)
axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

plt.show()
plt.savefig('../svg_figures/sensitivity_temp_flow.svg')
