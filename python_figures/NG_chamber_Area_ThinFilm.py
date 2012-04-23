#backend = 'svg'
execfile('std_header.py')

data = {}
#M44
cursor.execute("SELECT x/1000,y*1e9 FROM xy_values_microreactorNG where measurement = 1104")

data['M44'] = np.array(cursor.fetchall())

#CO Flow
cursor.execute("SELECT x/1000,y FROM xy_values_microreactorNG where measurement = 1114")
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

del titrations[0] #Remove the initial CO dosing
print len(titrations)

i = 0
for row in titrations:
    while data['M44'][i,0] <row:
        i = i+1
    times.append(i)


axis_array = []
fig = plt.figure()

print len(times)

#for i in range(0,len(times)):
for i in range(0,7):
    axis_array.append(fig.add_subplot(2,4,i+1))
    start = times[i]+30
    end = times[i]+145
    mean_y = [sum(data['M44'][start:start+20,1])/20,sum(data['M44'][end-20:end,1])/20]
    mean_x = [data['M44'][start+20,0],data['M44'][end-20,0]]
    axis_array[i].plot(data['M44'][start:end,0], data['M44'][start:end,1], 'r-')
    axis_array[i].plot(mean_x, mean_y, 'b-')
    axis_array[i].set_ylim(0,0.5)
    
    #axis_array[i].plot(data['M44'][start+650:end+600,0]-4300, data['M44'][start+650:end+600,1], 'g-')    
    
    #axis_array[i].set_xlim(data['M44'][start,0],data['M44'][end,0])
    
    f2 = interp1d([start,end], mean_y)
    charge = 0
    for j in range(start,end):
        #charge = charge + data['M44'][j,1]*(data['M44'][j,0]-data['M44'][j-1,0]) - f2(j)
        charge = charge + (data['M44'][j,1]-f2(j))*(data['M44'][j,0]-data['M44'][j-1,0])
    print charge
    
    axis_array[i].text(0.15, 0.8,round(charge,2),horizontalalignment='center',verticalalignment='center',transform = axis_array[i].transAxes,fontsize=10)
    
    axis_array[i].tick_params(direction='in', length=6, width=2, colors='k',labelsize=8,axis='both',pad=5)
    
#axis_array[0].set_ylabel('Ion Current / nA', fontsize=20)
#axis_array[0].set_xlabel('Time / s', fontsize=20)



#plt.tight_layout()
plt.show()
#plt.savefig('../svg_figures/oscillations_gas_dependence.svg')
#plt.savefig('thin_film_areas.png',dpi=300)