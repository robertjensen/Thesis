#backend = 'svg'
execfile('std_header.py')

import sensitivity_parameters as sens_parm

def DoTheFit(fit_x,fit_y,prefactor):
    fitfunc = lambda p, x: p[0]*np.e**(-1*p[1]/x)       # Target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
    p0 = [prefactor,10000] # Initial guess for the parameters
    p1, success = optimize.leastsq(errfunc, p0[:], args=(temp_interp(fit_x)+273.15,fit_y),maxfev=1000)
    return p1,success


parameters = sens_parm.parameters

data = {}

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room) 
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.1)

ratio = 1
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

oxygen_factor = 8.2e-3
bg = 0.12

axis = fig.add_subplot(1,1,1)

for i in range(0,len(parameters)):
    p = parameters[i]
    print p.name
    cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = " + p.m32 + " and x between " + p.xlow + " and " + p.xhigh)
    data['M32'] =  np.array(cursor.fetchall())
    cursor.execute("SELECT x/60000,y*1e9 FROM xy_values_microreactorNG where measurement = " + p.m44 + " and x between " + p.xlow + " and " + p.xhigh)
    data['M44'] =  np.array(cursor.fetchall())
    cursor.execute("SELECT x/60000,y FROM xy_values_microreactorNG where measurement = " + p.temperature)
    data['TEMPERATURE'] =  np.array(cursor.fetchall())

    temp_interp = interpolate.interp1d(data['TEMPERATURE'][:,0],data['TEMPERATURE'][:,1], bounds_error=False)
    m32_interp = interpolate.interp1d(data['M32'][:,0],data['M32'][:,1], bounds_error=False)
    #m44_interp = interpolate.interp1d(data['M44'][:,0],data['M44'][:,1], bounds_error=False)
    
    x_values = 1000.0/(273.15+temp_interp(data['M44'][:,0]))
    y_values = data['M44'][:,1]-bg-oxygen_factor*m32_interp(data['M44'][:,0])
    m44_interp = interpolate.interp1d(data['M44'][:,0],y_values, bounds_error=False)

    axis.plot(x_values, y_values, p.color)
    
    fit_x = np.linspace(p.fitx[0]/60000,p.fitx[1]/60000,100)
    fit_x_values = 273.15+temp_interp(fit_x)
    fit_plot_values = np.linspace(500,700,500)
    fitfunc = lambda p, x: p[0]*np.e**(-1*p[1]/x)       # Target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
    p0 = [p.prefactor,10000] # Initial guess for the parameters
    p1, success = optimize.leastsq(errfunc, p0[:], args=(fit_x_values,m44_interp(fit_x)),maxfev=1000)
    print success
    axis.plot(1000.0/fit_plot_values, fitfunc(p1,fit_plot_values), 'k-')

    #print temp_interp(fit_x)
    

axis.set_yscale('log')
#axis.set_xlim(1.4,2.4)
#axis.set_ylim(1e-2,20)

axis.set_ylabel('SEM Current / nA', fontsize=d.y_axis_font)
axis.set_xlabel('1000K / Temperature', fontsize=d.y_axis_font)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)


plt.show()
#plt.savefig('../svg_figures/sensitivity_background_correction_complete.svg')