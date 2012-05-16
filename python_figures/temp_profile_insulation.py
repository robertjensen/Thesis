backend = 'svg'
execfile('std_header.py')

fig = plt.figure()
fig.subplots_adjust(left=d.left_room) 
fig.subplots_adjust(bottom=d.bottom_room)
fig.subplots_adjust(right=d.right_room) 

ratio = d.ratio
fig_width = d.width
fig_width = fig_width /2.54     # width in cm converted to inches
fig_height = fig_width*ratio
fig.set_size_inches(fig_width,fig_height)

data = {}
data['IR213'] = []
f = open('IR_0213_profil.txt', 'r')
for line in f:
    numbers  = line.split()
    data['IR213'].append((tuple(float(number) for number in numbers)))
f.close()
data['IR213'] = np.array(data['IR213'])

data['IR217'] = []
f = open('IR_0217_profil.txt', 'r')
for line in f:
    numbers  = line.split()
    data['IR217'].append((tuple(float(number) for number in numbers)))
f.close()
data['IR217'] = np.array(data['IR217'])

arrow = dict(facecolor='black', shrink=0.05,width=1)
arrow = dict(facecolor='black',arrowstyle='->')
font = d.arrowfont-1

axis = fig.add_subplot(1,1,1)
axis.plot(data['IR213'][:,0]/5.47, data['IR213'][:,1]*0.95, 'r-')
axis.plot(data['IR217'][:,0]/6.07, data['IR217'][:,1]*0.9, 'b-')

axis.axvline(x=5.2,color='k')
axis.axvline(x=15.2,color='k')
axis.set_xlim(0,18)
axis.set_ylim(50,300)
axis.grid(False)

axis.annotate('250$^\circ$C', xy=(8, 249),  xycoords='data', xytext=(11, 200), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)
axis.annotate('300$^\circ$C', xy=(8, 299),  xycoords='data', xytext=(11, 270), textcoords='data', arrowprops=arrow, horizontalalignment='right', verticalalignment='top',fontsize=font,)

axis.tick_params(direction='in', length=d.ticklength, width=2, colors='k',labelsize=d.labelsize,axis='both',pad=d.pad)

axis.set_ylabel('Temperature / $^\circ$C', fontsize=d.y_axis_font)
axis.set_xlabel('Position / mm', fontsize=d.x_axis_font)

#plt.show()
plt.savefig('../svg_figures/temp_profile_insulation.svg')