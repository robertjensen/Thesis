import matplotlib
from scipy import optimize
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MySQLdb
from scipy import interpolate
import math
from matplotlib.backends.backend_pdf import PdfPages

matplotlib.rc('text',usetex=True) # Magic fix for the font warnings

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")


def DoTheFit(fit_x,fit_y,prefactor):
    fitfunc = lambda p, x: p[0]*np.e**(-1*p[1]/x)       # Target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
    p0 = [prefactor,10000] # Initial guess for the parameters
    p1, success = optimize.leastsq(errfunc, p0[:], args=(temp_interp(fit_x)+273.15,fit_y),maxfev=1000)
    return p1,success

class dataHolder:
    pass

parameters = []

N5_up = dataHolder()
N5_up.name = "N5 up"
N5_up.m44 = "497"
N5_up.pressure = "498"
N5_up.temperature = "502"
N5_up.xlow = "6500000"
N5_up.xhigh = "15850000"
N5_up.fitx = [13500000,14000000]
N5_up.prefactor = 0.0037
N5_up.ae = 9546
N5_up.M44_ini = 5.4662794434e-10
N5_up.color = "m-"
N5_up.P_ini = 2.067e-7
N5_up.area = 38
parameters.append(N5_up)

N5_down = dataHolder()
N5_down.name = "N5 down"
N5_down.m44 = "497"
N5_down.pressure = "498"
N5_down.temperature = "502"
N5_down.xlow = "15850000" 
N5_down.xhigh = "22000000"
N5_down.fitx = [16000000,17000000]
N5_down.color = "m--"
N5_down.prefactor = 0.0014
N5_down.M44_ini = 5.4662794434e-10
N5_down.P_ini = 2.067e-7
N5_down.area = 38
parameters.append(N5_down)

N8_up = dataHolder()
N8_up.name = "N8 up"
N8_up.m44 = "458"
N8_up.pressure = "459"
N8_up.temperature = "463"
N8_up.xlow = "9200000"
N8_up.xhigh = "16400000"
N8_up.fitx = [14000000,15000000]
N8_up.color = "b-"
N8_up.prefactor = 0.1
N8_up.P_ini = 2.022e-7
N8_up.M44_ini = 5.3035797149e-10
N8_up.area = 707
parameters.append(N8_up)

N8_down = dataHolder()
N8_down.name = "N8 down"
N8_down.m44 = "458"
N8_down.pressure = "459"
N8_down.temperature = "463"
N8_down.xlow = "16400000" 
N8_down.xhigh = "24000000"
N8_down.fitx = [18000000,19000000]
N8_down.color = "b--"
N8_down.prefactor = 0.001
N8_down.P_ini = 2.022e-7
N8_down.M44_ini = 5.3035797149e-10
N8_down.area = 707
parameters.append(N8_down)

N9_up = dataHolder()
N9_up.name = "N9 up"
N9_up.m44 = "445"
N9_up.pressure = "446"
N9_up.temperature = "450"
N9_up.xlow = "5850000"
N9_up.xhigh = "12100000"
N9_up.fitx = [10500000,11000000]
N9_up.prefactor = 0.0004
N9_up.M44_ini = 4.9065010139e-10
N9_up.color = "g-"
N9_up.P_ini = 1.987e-7
N9_up.area = 1960
parameters.append(N9_up)

N10_up = dataHolder()
N10_up.name = "N10 up"
N10_up.m44 = "313"
N10_up.pressure = "314"
N10_up.temperature = "318"
N10_up.xlow = "6000000"
N10_up.xhigh = "12000000"
N10_up.fitx = [10500000,11000000]
N10_up.color = "c-"
N10_up.prefactor = 0.01
N10_up.M44_ini = 6.8808298397e-10
N10_up.P_ini = 1.977e-7
N10_up.area = 7850
parameters.append(N10_up)

#N10_down unreliable due to bad temperature measurement
#N10_down = dataHolder()
#N10_down.name = "N10 down"
#N10_down.m44 = "313"
#N10_down.pressure = "314"
#N10_down.temperature = "318"
#N10_down.xlow = "12500000"
#N10_down.xhigh = "18500000"
#N10_down.prefactor = 0.001 # Not adapted for this parameter
#N10_down.M44_ini = 5.3035797149e-10 # Not adapted for this parameter
#N10_down.color = "c--"
#N10_down.P_ini = 1.977e-7
#N10_down.M44_ini = 6.8808298397e-10
#N10_down.area = 7850
#parameters.append(N10_down)

N11_up = dataHolder()
N11_up.name = "N11 up"
N11_up.m44 = "342"
N11_up.pressure = "343"
N11_up.temperature = "347"
N11_up.xlow = "6800000"
N11_up.xhigh = "12500000"
N11_up.fitx = [9500000,10000000]
N11_up.color = "r-"
N11_up.prefactor = 4.6
N11_up.P_ini = 1.756e-07
N11_up.M44_ini = 2.8776756951e-10
N11_up.area = 196000
parameters.append(N11_up)

#N11_down = dataHolder()
#N11_down.name = "N11 down"
#N11_down.m44 = "342"
#N11_down.pressure = "343"
#N11_down.temperature = "347"
#N11_down.xlow = "12500000"
#N11_down.xhigh = "18000000"
#N11_down.fitx = [150,200]
#N11_down.color = "r--"
#N11_down.P_ini = 1.756e-07
#N11_down.M44_ini = 2.8776756951e-10
#N11_down.area = 196000
#parameters.append(N11_down)


#colors = ['r-','b-','g-','c-','m-','y-','r--','b--','g--','c--','m--','y--']

fig = plt.figure()
fig.subplots_adjust(top=0.85) # Make room for x-label
fig.subplots_adjust(bottom=0.15) # Make room for x-label
fig.subplots_adjust(right=0.95) # Make room for second y-label

ratio = 0.61803398           # Golden mean
fig_width = 9
fig_width = fig_width /2.54        # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

cursor = db.cursor()
data = {}
fit_params = np.zeros((len(parameters),7))
axis = fig.add_subplot(1,1,1)

pp = PdfPages('multipage.pdf')
for i in range(0,len(parameters)):

    pdffig = plt.figure()
    pdffig.subplots_adjust(wspace=0.3) # Make room for x-label
    pdffig.subplots_adjust(hspace=0.3) # Make room for x-label

    P = parameters[i]

    cursor.execute("SELECT x,y FROM xy_values_microreactorNG where measurement = " + P.m44 + " and x between " + P.xlow + " and " + P.xhigh)
    data['M44'] = np.array(cursor.fetchall())
    cursor.execute("SELECT x,y FROM xy_values_microreactorNG where measurement = " + P.pressure + " and x between " + P.xlow + " and " + P.xhigh)
    data['PRESSURE'] =  np.array(cursor.fetchall())
    cursor.execute("SELECT x,y FROM xy_values_microreactorNG where measurement = " + P.temperature + " and x between " + P.xlow + " and " + P.xhigh)
    data['TEMPERATURE'] = np.array(cursor.fetchall())

    x_data = data['M44'][:,0]
    y_data = data['M44'][:,1]
    temp_interp = interpolate.interp1d(data['TEMPERATURE'][:,0],data['TEMPERATURE'][:,1], bounds_error=False)
    press_interp = interpolate.interp1d(data['PRESSURE'][:,0],data['PRESSURE'][:,1], bounds_error=False)
    ydata_interp = interpolate.interp1d(x_data,y_data, bounds_error=False)

    max_temp = max(data['TEMPERATURE'][:,1])
    min_temp = min(data['TEMPERATURE'][:,1])
    
    #Short-hand to the pressure corrected y-data
    y_data_pc = P.P_ini *y_data / press_interp(x_data)
    ydata_pc_interp = interpolate.interp1d(x_data,y_data_pc, bounds_error=False)

    #P.M44_ini = P.P_ini *  P.M44_ini / press_interp(50)

    # Make the fit
    print i
    fit_x = range(P.fitx[0],P.fitx[1])
    fit_y = ydata_interp(fit_x)
    p1,success = DoTheFit(fit_x,fit_y,P.prefactor)

    fit_y = ydata_pc_interp(fit_x)
    p1_pc,success = DoTheFit(fit_x,fit_y,P.prefactor)
    
    fit_y = ydata_pc_interp(fit_x)
    p1_pc_bg,success = DoTheFit(fit_x,fit_y-P.M44_ini,P.prefactor)
    
    fit_params[i,0] = P.area
    fit_params[i,1] = p1[0]
    fit_params[i,2] = p1[1]
    fit_params[i,3] = p1_pc[0]
    fit_params[i,4] = p1_pc[1]
    fit_params[i,5] = p1_pc_bg[0]
    fit_params[i,6] = p1_pc_bg[1]
    
    #k = 5
    #while temp_interp(x_data[k])<50:
    #    k = k+1
    #print k
    #print temp_interp(x_data[k])
    #print y_data[k]

    #Un-modified M44-signal and temperature
    pdf_axis = pdffig.add_subplot(4,3,1)
    pdf_axis.plot(x_data/1e6,y_data,'g-',label="M44-raw")
    pdf_axis2 = pdf_axis.twinx()
    pdf_axis2.plot(data['TEMPERATURE'][:,0]/1e6,data['TEMPERATURE'][:,1],'b-',label="Temperature")
    pdf_axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=6,axis='both',pad=5)
    pdf_axis2.tick_params(direction='in', length=2, width=1, colors='k',labelsize=6,axis='both',pad=5)
    pdf_axis.annotate("M44 raw", (0.1,0.9),xycoords='axes fraction',fontsize=6)


    #Un-modified pressure and temperature    
    pdf_axis = pdffig.add_subplot(4,3,2)
    pdf_axis.plot(data['PRESSURE'][:,0]/1e6,data['PRESSURE'][:,1],'r-')
    pdf_axis2 = pdf_axis.twinx()
    pdf_axis2.plot(data['TEMPERATURE'][:,0]/1e6,data['TEMPERATURE'][:,1])
    pdf_axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=6,axis='both',pad=5)
    pdf_axis2.tick_params(direction='in', length=2, width=1, colors='k',labelsize=6,axis='both',pad=5)
    pdf_axis.annotate("Pressure", (0.1,0.9),xycoords='axes fraction',fontsize=6)
    
    #M44-log and M44-log pressure corrected and M44-log pressure and bg corrected as a function of temperature
    pdf_axis = pdffig.add_subplot(4,3,3)
    pdf_axis.plot(temp_interp(x_data), np.log10(y_data), 'g-')
    pdf_axis.plot(temp_interp(x_data), np.log10(y_data_pc), 'g--')
    pdf_axis.plot(temp_interp(x_data), np.log10(y_data-P.M44_ini), 'm--')
    pdf_axis.plot(temp_interp(x_data), np.log10(y_data_pc-P.M44_ini), 'm-')
    pdf_axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=6,axis='both',pad=5)
    pdf_axis.set_ylim(-11,-7)
    pdf_axis.annotate("M44(sol.)", (0.1,0.9),xycoords='axes fraction',fontsize=6)
    pdf_axis.annotate("M44PC(dash)", (0.1,0.8),xycoords='axes fraction',fontsize=6)
    pdf_axis.annotate("M44BG(mag. dash.)", (0.1,0.7),xycoords='axes fraction',fontsize=6)
    pdf_axis.annotate("M44PC BG(mag. sol.)", (0.1,0.6),xycoords='axes fraction',fontsize=6)

    #Arrhenius and corresponding fit
    pdf_axis = pdffig.add_subplot(4,3,4)
    pdf_axis.plot(1000.0/(temp_interp(x_data)+273.15), np.log10(y_data), 'g-')    
    pdf_axis.plot(1000.0/(temp_interp(x_data)+273.15), np.log10(p1[0]*np.e**(-1*p1[1]/(temp_interp(x_data)+273.15))), 'k-')
    pdf_axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=6,axis='both',pad=5)
    #pdf_axis.set_xlim(1,2.5)
    pdf_axis.set_xlim(1000.0/(max_temp+273.15),1000.0/(min_temp+273.15))
    pdf_axis.set_ylim(-10,-7.5)
    pdf_axis.annotate("Arrhenious - raw", (0.1,0.8),xycoords='axes fraction',fontsize=6)    
    
    #Arrhenius and corresponding fit - pressure corrected
    pdf_axis = pdffig.add_subplot(4,3,5)
    pdf_axis.plot(1000.0/(temp_interp(x_data)+273.15), np.log10(y_data_pc), 'g-')    
    pdf_axis.plot(1000.0/(temp_interp(x_data)+273.15), np.log10(p1_pc[0]*np.e**(-1*p1_pc[1]/(temp_interp(x_data)+273.15))), 'k-')
    pdf_axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=6,axis='both',pad=5)
    #pdf_axis.set_xlim(1,2.5)
    pdf_axis.set_xlim(1000.0/(max_temp+273.15),1000.0/(min_temp+273.15))
    pdf_axis.set_ylim(-10,-7.5)
    pdf_axis.annotate("ArrheniousPC", (0.1,0.8),xycoords='axes fraction',fontsize=6)    


    #Arrhenius and corresponding fit - pressure corrected and BG corrected
    pdf_axis = pdffig.add_subplot(4,3,6)
    pdf_axis.plot(1000.0/(temp_interp(x_data)+273.15), np.log10(y_data_pc-P.M44_ini), 'g-')    
    pdf_axis.plot(1000.0/(temp_interp(x_data)+273.15), np.log10(p1_pc_bg[0]*np.e**(-1*p1_pc_bg[1]/(temp_interp(x_data)+273.15))), 'k-')
    pdf_axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=6,axis='both',pad=5)
    pdf_axis.set_xlim(1000.0/(max_temp+273.15),1000.0/(min_temp+273.15))
    pdf_axis.set_ylim(-10,-7.5)
    pdf_axis.annotate("ArrheniousPC-BG", (0.1,0.8),xycoords='axes fraction',fontsize=6)    

    #Arrhenius and corresponding fit - misfit
    pdf_axis = pdffig.add_subplot(4,3,7)
    pdf_axis.plot(1000.0/(temp_interp(x_data)+273.15), np.log10(y_data) - np.log10(p1[0]*np.e**(-1*p1[1]/(temp_interp(x_data)+273.15))), 'k-')
    pdf_axis.plot(1000.0/(temp_interp(x_data)+273.15), np.log10(y_data_pc) - np.log10(p1_pc[0]*np.e**(-1*p1_pc[1]/(temp_interp(x_data)+273.15))), 'k--')
    pdf_axis.plot(1000.0/(temp_interp(x_data)+273.15), np.log10(y_data_pc-P.M44_ini) - np.log10(p1_pc_bg[0]*np.e**(-1*p1_pc_bg[1]/(temp_interp(x_data)+273.15))), 'm-')
    pdf_axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=6,axis='both',pad=5)
    pdf_axis.set_xlim(1000.0/(max_temp+273.15),1000.0/(min_temp+273.15))
    pdf_axis.set_ylim(-1,1)
    pdf_axis.annotate("Misfit", (0.1,0.9),xycoords='axes fraction',fontsize=6)
    pdf_axis.annotate("PC misfit (dashed)", (0.1,0.8),xycoords='axes fraction',fontsize=6)
    pdf_axis.annotate("PC and bg misfit (mag.)", (0.1,0.7),xycoords='axes fraction',fontsize=6)

    #Fitting region
    pdf_axis = pdffig.add_subplot(4,3,8)
    pdf_axis.plot(temp_interp(x_data), np.log10(y_data), 'g-')
    pdf_axis.plot([temp_interp(P.fitx[0]),temp_interp(P.fitx[0])], [-10,-6], 'k-')
    pdf_axis.plot([temp_interp(P.fitx[1]),temp_interp(P.fitx[1])], [-10,-6], 'k-')
    pdf_axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=6,axis='both',pad=5)

    plt.savefig(pp, format='pdf')
    plt.close()

    #Make the arrhenius plot
    axis.plot(1000.0/(temp_interp(x_data)+273.15), np.log10((y_data_pc-P.M44_ini)/P.area), P.color,linewidth=0.75)
    #axis.plot(1.0/(temp_interp(x_data)+273.15), np.log10((p1_pc[0]*np.e**(-1*p1_pc[1]/(temp_interp(x_data)+273.15)))/P.area), 'k-')

pp.close()
axis.grid(False)    

#arrow = dict(facecolor='black',arrowstyle='->')
#axis.annotate('M28', xy=(830, 0.85),  xycoords='data', xytext=(800, 0.95), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=9,)

axis.tick_params(direction='in', length=6, width=1, colors='k',labelsize=8,axis='both',pad=3)
axis.set_ylabel('Turn Over Frequency (a.u.)', fontsize=8)
axis.set_xlabel('1000 / Temperature (K)', fontsize=8)
axis.set_xticks((1.5,1.75,2.0,2.25,2.5,2.75))
axis.set_xlim(1.4,3)
axis.set_ylim(-16,-9)

arrow = dict(facecolor='black',arrowstyle='->')
axis.annotate('196.000', xy=(2.45, -15.2),  xycoords='data', xytext=(2.3, -15.4), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=6,)
axis.annotate('7.850', xy=(2.5, -13.7),  xycoords='data', xytext=(2.6, -14.5), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=6,)
axis.text(2.5,-13.25,'1960',fontsize=6,)
axis.annotate('707', xy=(2.3, -12.6),  xycoords='data', xytext=(2.6, -12), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=6,)
axis.annotate('38', xy=(2.5, -11.3),  xycoords='data', xytext=(2.3, -10.5), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='center',fontsize=6,)


temp_ticks = np.array([100,150,200,250,300,350])

axis3 = axis.twiny()
axis3.set_xticks(1000.0/(temp_ticks+273.15))
axis3.set_xticklabels(temp_ticks)
axis3.set_xlim(1.4,3)
axis3.set_xlabel('Temperature', fontsize=8)
axis3.tick_params(direction='in', length=2, width=1, colors='k',labelsize=8,axis='both',pad=3)


#plt.tight_layout()
#plt.show()
plt.savefig('../arrhenius.png',dpi=300)

del fig

fig = plt.figure()
fig.subplots_adjust(bottom=0.2) # Make room for x-label
fig.subplots_adjust(right=0.85) # Make room for second y-label

ratio = 0.61803398           # Golden mean
fig_width = 9
fig_width = fig_width /2.54        # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

cursor = db.cursor()
axis = fig.add_subplot(1,1,1)

#axis.plot(fit_params[:,0],fit_params[:,1],'bo')
#axis.plot(fit_params[:,0],fit_params[:,2],'ro')
axis.loglog(fit_params[:,0],fit_params[:,1],'b^')
axis.loglog(fit_params[:,0],fit_params[:,3],'bv')
axis.loglog(fit_params[:,0],fit_params[:,5],'bo')
axis.set_ylabel('Prefactor', fontsize=8)
axis2 = axis.twinx()
axis2.loglog(fit_params[:,0],fit_params[:,2],'r^')
axis2.loglog(fit_params[:,0],fit_params[:,4],'rv')
axis2.loglog(fit_params[:,0],fit_params[:,6],'ro')
axis.set_ylabel('Activation Energy (a.u.) (red)', fontsize=8)
print fit_params[0]

plt.show()
