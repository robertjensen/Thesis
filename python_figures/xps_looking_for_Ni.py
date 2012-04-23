#backend = 'svg'
execfile('std_header.py')

data = {}
#Silicon
cursor.execute("SELECT x,y FROM xy_values_bifrost where measurement = 3189")
data['si'] = np.array(cursor.fetchall())

#Platinum
cursor.execute("SELECT x,y FROM xy_values_bifrost where measurement = 3188")
data['pt'] =  np.array(cursor.fetchall())

axis_array = []
fig = plt.figure()

arrow = dict(facecolor='black', shrink=0.05,width=1)
font = d.arrowfont

for i in range(0,1):
    axis_array.append(fig.add_subplot(1,1,i+1))
    axis_array[i].plot(data['si'][:,0], data['si'][:,1], 'r-')
    axis_array[i].plot(data['pt'][:,0], data['pt'][:,1], 'b-')
    axis_array[i].set_xlim(1100,0)
    
    axis_array[i].annotate('O KLL', xy=(975, 18000),  xycoords='data', xytext=(900, 32000), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
    axis_array[i].annotate('Ni 2p', xy=(860, 17000),  xycoords='data', xytext=(860, 38000), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
    axis_array[i].annotate('O 1s', xy=(535, 48000),  xycoords='data', xytext=(590, 45000), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
    axis_array[i].annotate('Pt 4p3/2', xy=(521, 17000),  xycoords='data', xytext=(390, 27000), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)    
    axis_array[i].annotate('Ti 2p', xy=(460, 17000),  xycoords='data', xytext=(370, 25000), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
    axis_array[i].annotate('Pt 4d', xy=(322, 16000),  xycoords='data', xytext=(322, 30000), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)        
    axis_array[i].annotate('Pt 4f', xy=(70, 18000),  xycoords='data', xytext=(90, 32000), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
    axis_array[i].annotate('Si 2p', xy=(105, 11000),  xycoords='data', xytext=(130, 20000), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
    axis_array[i].annotate('Si 2s', xy=(152, 10000),  xycoords='data', xytext=(190, 15000), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
    axis_array[i].annotate('C 1s', xy=(286, 26000),  xycoords='data', xytext=(220, 32000), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
    #axis_array[i].annotate('O 2s', xy=(28, 2000),  xycoords='data', xytext=(20, 9000), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)    
    
    axis_array[i].tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)
    
axis_array[0].set_ylabel('Counts / s', fontsize=d.y_axis_font)
axis_array[0].set_xlabel('Binding Energy / eV', fontsize=d.x_axis_font)



#plt.tight_layout()
plt.show()
plt.savefig('../svg_figures/xps_looking_for_Ni.svg')