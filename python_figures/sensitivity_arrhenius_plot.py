backend = 'svg'
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
fig.subplots_adjust(right=d.right_room*0.95) 
fig.subplots_adjust(hspace=0.1)
fig.subplots_adjust(wspace=0.1)

ratio = 1
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

oxygen_factor = 8.2e-3
bg = 0.12


axis = fig.add_subplot(2,1,1)
axis_sub = fig.add_subplot(2,1,2)
for i in range(0,len(parameters)):
    p = parameters[i]
    #print p.name
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

    #axis.plot(x_values, y_values, p.color)
    
    fit_x = np.linspace(p.fitx[0]/60000,p.fitx[1]/60000,100)
    fit_x_values = 273.15+temp_interp(fit_x)

    fit_x_errorbar = np.linspace((p.fitx_eb[0])/60000,(p.fitx_eb[1])/60000,100)
    fit_x_values_errorbar = 273.15+temp_interp(fit_x_errorbar)
    
    fit_plot_values = np.linspace(500,700,500)
    fitfunc = lambda p, x: p[0]*np.e**(-1*p[1]/x)       # Target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
    p0 = [p.prefactor,10000] # Initial guess for the parameters
    p1, success = optimize.leastsq(errfunc, p0[:], args=(fit_x_values,m44_interp(fit_x)),maxfev=1000)

    p1_errorbar, success = optimize.leastsq(errfunc, p0[:], args=(fit_x_values_errorbar,m44_interp(fit_x_errorbar)),maxfev=1000)

    #print p1
    #axis.plot(1000.0/fit_plot_values, fitfunc(p1,fit_plot_values), 'k-')
    #axis.plot(1000.0/fit_x_values_errorbar, np.log10(fitfunc(p1_errorbar,fit_x_values_errorbar)), 'y-',linewidth=3)
    axis.plot(1000.0/fit_x_values, np.log10(fitfunc(p1,fit_x_values)), 'k-',linewidth=2)
    p.ae = p1[1]
    p.prefactor = p1[0]

    p.ae_eb = p1_errorbar[1]
    p.prefactor_eb = p1_errorbar[0]

    #print p.prefactor_eb - p.prefactor

    #print temp_interp(fit_x)
    axis.plot(x_values, np.log10(y_values), p.color)
    
    axis_sub.plot(x_values, np.log10(y_values/p.area), p.color)

    
yticks = np.array([0.1,1,10])
axis.set_yticks(np.log10(yticks))
axis.set_yticklabels(yticks)
axis.set_xlim(1.4,2.4)
axis.set_ylim(np.log10(1e-1),np.log10(20))
axis.set_ylabel('SEM Current / nA', fontsize=d.y_axis_font)
axis.set_xticklabels([])

axis2 = axis.twinx()
yticks = np.array([1e12,1e13,1e14])
yticks_s = ["10$^{12}$","10$^{13}$","10$^{14}$"]
axis2.set_ylim(np.log10(1e-1),np.log10(20))
axis2.set_yticks(np.log10(yticks*1.6e-13))
axis2.set_yticklabels(yticks_s)
axis2.set_ylabel('Total Conversion / s$^{-1}$', fontsize=d.y_axis_font)
axis2.set_xticklabels([])
axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis2.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

## Setup of second plot
yticks = np.array([1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1])
yticks_s = ["10$^{-7}$","10$^{-6}$","10$^{-5}$","10$^{-4}$","10$^{-3}$","10$^{-2}$","10$^{-1}$"]
axis_sub.set_ylim(-7.1,-0.9)
axis_sub.set_yticks(np.log10(yticks))
axis_sub.set_yticklabels(yticks_s)
axis_sub.set_xlim(1.4,2.4)
axis_sub.set_ylabel('SEM/area / nA/($\mu$m)$^2$', fontsize=d.y_axis_font)
axis_sub.set_xlabel('1000K / Temperature', fontsize=d.y_axis_font)

axis2_sub = axis_sub.twinx()
yticks = np.array([1e6,1e7,1e8,1e9,1e10,1e11,1e12])
yticks_s = ["10$^{6}$","10$^{7}$","10$^{8}$","10$^{9}$","10$^{10}$","10$^{11}$","10$^{12}$"]
axis2_sub.set_ylim(-7.1,-0.9)
axis2_sub.set_yticks(np.log10(yticks*1.6e-13))
axis2_sub.set_yticklabels(yticks_s)
axis2_sub.set_ylabel('Conversion / s$^{-1}$ $\cdot$ ($\mu$m)$^{-2}$', fontsize=d.y_axis_font)

axis_sub.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis2_sub.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)


#plt.show()
plt.savefig('../svg_figures/sensitivity_arrhenius.svg')

del fig

ae_list_up = []
ae_list_down = []
ae_list_up_eb = []
ae_list_down_eb = []

for i in range(0,len(parameters)):
    p = parameters[i]
    if p.name.endswith("down"):
        ae_list_down.append([p.area,p.ae,p.prefactor/(p.area/6.5e6),p.prefactor_eb/(p.area/6.5e6),p.ae_eb])
    else:
        ae_list_up.append([p.area,p.ae,p.prefactor/(p.area/6.5e6),p.prefactor_eb/(p.area/6.5e6),p.ae_eb])
    
ae_list_up =  np.array(ae_list_up)
ae_list_down =  np.array(ae_list_down)

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room*0.7)
fig.subplots_adjust(right=d.right_room*0.95) 
fig.subplots_adjust(hspace=0.1)
fig.subplots_adjust(wspace=0.1)

ratio = 1
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)
axis = fig.add_subplot(2,1,1)
axis_sub = fig.add_subplot(2,1,2)

Kb = 8.617e-5

axis.plot(ae_list_up[:,0],ae_list_up[:,1]*Kb, 'ko-')
axis.plot(ae_list_down[:,0],ae_list_down[:,1]*Kb, 'k*-')
axis.set_ylim(0.9,1.4)
axis.set_ylabel('Activation Energy / eV', fontsize=d.y_axis_font)
axis_sub.set_xlabel('Pt spot area / ($\mu$m)$^2$', fontsize=d.y_axis_font)
axis.set_xscale('log')

#axis2 = axis.twinx()
#axis2.plot(ae_list_up[:,0],ae_list_up[:,2]*1.6e-13, 'ro-')
#axis2.plot(ae_list_down[:,0],ae_list_down[:,2]*1.6e-13, 'r*-')

#axis_sub.plot(ae_list_up[:,0],ae_list_up[:,2], 'ro-')
#axis_sub.plot(ae_list_down[:,0],ae_list_down[:,2], 'r*-')

axis_sub.plot(ae_list_up[:,0],ae_list_up[:,2], 'ko-')
axis_sub.plot(ae_list_down[:,0],ae_list_down[:,2], 'k*-')

for eb in ae_list_up:
    corr = eb[3]/eb[2]
    axis_sub.plot([eb[0],eb[0]],[eb[2]/corr,eb[2]*corr], 'r-')
    
    corr = eb[4]/eb[1]
    axis.plot([eb[0],eb[0]],[Kb*eb[1]/corr,Kb*eb[1]*corr], 'r-')


for eb in ae_list_down:
    corr = eb[3]/eb[2]
    axis_sub.plot([eb[0],eb[0]],[eb[2]/corr,eb[2]*corr], 'r-')

    corr = eb[4]/eb[1]
    axis.plot([eb[0],eb[0]],[Kb*eb[1]/corr,Kb*eb[1]*corr], 'r-')


axis_sub.set_ylim(1e12,1e16)

axis_sub.set_ylabel('Prefactor / site$^{-1}$ $\cdot$ s$^{-1}$', fontsize=d.y_axis_font)
axis_sub.set_yscale('log')
axis_sub.set_xscale('log')

axis.set_xticklabels([])

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
axis_sub.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)


#plt.show()
plt.savefig('../svg_figures/sensitivity_activation_energies.svg')