backend = 'svg'
execfile('std_header.py')

sys.path.append('area_measurements')
import MR102_approx20cov_5_2nm as config

#matplotlib.rc('text',usetex=False) # Magic fix for the font warnings

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room) 

ratio = 1.7
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

data = {}
cursor.execute(config.M44)
data['M44'] = np.array(cursor.fetchall())
cursor.execute(config.CO_FLOW)
data['CO_FLOW'] =  np.array(cursor.fetchall())

i = 0
old_m44 = 0
titrations = [] #Holds the switching times
times = []
for row in data['CO_FLOW']:
    i = i+1
    if (row[1] > (0.5)) and (old_m44<0.5):
        titrations.append(row[0])
        old_m44 = row[1]
        
    if (i%10==0):
        old_m44 = row[1]

for i in config.skip:
    del titrations[i]
print len(titrations)

i = 0
for row in titrations:
    while data['M44'][i,0] <row:
        i = i+1
    times.append(i)


axis_array = []
charges = []
print len(times)

for i in range(0,len(times)):
    axis_array.append(fig.add_subplot(config.layout_y,config.layout_x,i+1))
    start = times[i]+config.start
    end = times[i]+config.end
    mean_y = [sum(data['M44'][start:start+20,1])/20,sum(data['M44'][end-20:end,1])/20]
    mean_x = [data['M44'][start+20,0],data['M44'][end-20,0]]
    axis_array[i].plot(data['M44'][start:end,0], data['M44'][start:end,1], 'r-')
    axis_array[i].plot(mean_x, mean_y, 'b-')
    axis_array[i].set_ylim(-0.01,0.1)
    if not i % config.layout_x == 0:
        axis_array[i].set_yticks([])
    else:
        axis_array[i].set_yticks([0,0.025,0.05,0.075])
    axis_array[i].set_xticks([])
    axis_array[i].ticklabel_format(useOffset=False)
    f2 = interpolate.interp1d([start,end], mean_y)
    charge = 0
    for j in range(start,end):
        charge = charge + (data['M44'][j,1]-f2(j))*(data['M44'][j,0]-data['M44'][j-1,0])
    print charge
    charges.append(charge)
    
    axis_array[i].text(0.15, 0.8,round(charge,2),horizontalalignment='center',verticalalignment='center',transform = axis_array[i].transAxes,fontsize=10)

    axis_array[i].tick_params(direction='in', right='off',length=d.ticklength, width=1, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
#axis_array[0].set_ylabel('Ion Current / nA', fontsize=d.y_axis_font)

#plt.tight_layout()
#plt.show()
plt.savefig('../svg_figures/area_MR102.svg')



del fig

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

x_axis = range(1,len(charges)+1)
axis.plot(x_axis[0:5],charges[0:5], 'go-')
axis.axvline(x=5.5,color='k')
axis.plot(x_axis[5:10],charges[5:10], 'ro-')
axis.axvline(x=15.5,color='k')
axis.plot(x_axis[10:15],charges[10:15], 'ro-')

#Mangler stadig helt at forstå behandlingen af denne prøve...

axis.set_ylim(0,10)
axis.set_xlabel('Measurement number', fontsize=d.x_axis_font)
axis.set_ylabel('Area / nC', fontsize=d.y_axis_font)
axis.tick_params(direction='in', right='off',length=d.ticklength, width=1, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

plt.savefig('../svg_figures/area_MR102_summary.svg')
