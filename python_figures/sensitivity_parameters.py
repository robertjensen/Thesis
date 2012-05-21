class dataHolder:
    pass

parameters = []

N5_up = dataHolder()
N5_up.name = "N5 up"
N5_up.m32 = "496"
N5_up.m44 = "497"
N5_up.pressure = "498"
N5_up.temperature = "502"
N5_up.xlow = "6500000"
N5_up.xhigh = "15850000"
N5_up.fitx = [13600000,14000000]
N5_up.prefactor = 2e8
N5_up.ae = 9546
N5_up.M44_ini = 5.4662794434e-10
N5_up.color = "m-"
N5_up.P_ini = 2.067e-7
N5_up.area = 38
parameters.append(N5_up)

N5_down = dataHolder()
N5_down.name = "N5 down"
N5_down.m32 = "496"
N5_down.m44 = "497"
N5_down.pressure = "498"
N5_down.temperature = "502"
N5_down.xlow = "15850000" 
N5_down.xhigh = "22000000"
N5_down.fitx = [16300000,16600000]
N5_down.color = "m--"
N5_down.prefactor = 2e8
N5_down.M44_ini = 5.4662794434e-10
N5_down.P_ini = 2.067e-7
N5_down.area = 38
parameters.append(N5_down)

N8_up = dataHolder()
N8_up.name = "N8 up"
N8_up.m32 = "457"
N8_up.m44 = "458"
N8_up.pressure = "459"
N8_up.temperature = "463"
N8_up.xlow = "9200000"
N8_up.xhigh = "16400000"
N8_up.fitx = [14400000,14900000]
N8_up.color = "b-"
N8_up.prefactor = 6e10
N8_up.P_ini = 2.022e-7
N8_up.M44_ini = 5.3035797149e-10
N8_up.area = 707
parameters.append(N8_up)

N8_down = dataHolder()
N8_down.name = "N8 down"
N8_down.m32 = "457"
N8_down.m44 = "458"
N8_down.pressure = "459"
N8_down.temperature = "463"
N8_down.xlow = "16400000" 
N8_down.xhigh = "24000000"
N8_down.fitx = [18000000,18600000]
N8_down.color = "b--"
N8_down.prefactor = 6e10
N8_down.P_ini = 2.022e-7
N8_down.M44_ini = 5.3035797149e-10
N8_down.area = 707
parameters.append(N8_down)

N9_up = dataHolder()
N9_up.name = "N9 up"
N9_up.m32 = "444"
N9_up.m44 = "445"
N9_up.pressure = "446"
N9_up.temperature = "450"
N9_up.xlow = "5850000"
N9_up.xhigh = "12100000"
N9_up.fitx = [11200000,11500000]
N9_up.prefactor = 2e10
N9_up.M44_ini = 4.9065010139e-10
N9_up.color = "g-"
N9_up.P_ini = 1.987e-7
N9_up.area = 1960
parameters.append(N9_up)

N10_up = dataHolder()
N10_up.name = "N10 up"
N10_up.m32 = "312"
N10_up.m44 = "313"
N10_up.pressure = "314"
N10_up.temperature = "318"
N10_up.xlow = "6000000"
N10_up.xhigh = "12000000"
N10_up.fitx = [10600000,10900000]
N10_up.color = "c-"
N10_up.prefactor = 4e13
N10_up.M44_ini = 6.8808298397e-10
N10_up.P_ini = 1.977e-7
N10_up.area = 7850
parameters.append(N10_up)

#N10_down unreliable due to bad temperature measurement
N10_down = dataHolder()
N10_down.name = "N10 down"
N10_down.m32 = "312"
N10_down.m44 = "313"
N10_down.pressure = "314"
N10_down.temperature = "318"
N10_down.xlow = "12500000"
N10_down.xhigh = "18500000"
N10_down.fitx = [13200000,13700000]
N10_down.prefactor = 4e13
N10_down.M44_ini = 5.3035797149e-10 # Not adapted for this parameter
N10_down.color = "c--"
N10_down.P_ini = 1.977e-7
N10_down.M44_ini = 6.8808298397e-10
N10_down.area = 7850
parameters.append(N10_down)

N11_up = dataHolder()
N11_up.name = "N11 up"
N11_up.m32 = "341"
N11_up.m44 = "342"
N11_up.pressure = "343"
N11_up.temperature = "347"
N11_up.xlow = "6800000"
N11_up.xhigh = "12500000"
N11_up.fitx = [9850000,10250000]
N11_up.color = "r-"
N11_up.prefactor = 5e12
N11_up.P_ini = 1.756e-07
N11_up.M44_ini = 2.8776756951e-10
N11_up.area = 196000
parameters.append(N11_up)

#N11_down = dataHolder()
#N11_down.name = "N11 down"
#N11_down.m32 = "341"
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
