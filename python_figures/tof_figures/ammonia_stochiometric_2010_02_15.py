temperatures = []

temperatures = temperatures + [40,60,80]

for i in range(100,195,5): #Note last value is not included
    temperatures = temperatures + [i]

for i in range(180,95,-5): #Note last value is not included
    temperatures = temperatures + [i]

for i in range(100,185,5): #Note last value is not included
    temperatures = temperatures + [i]

temperatures = temperatures + [190]

for i in range(180,95,-5): #Note last value is not included
    temperatures = temperatures + [i]

initial_db = 189

masses = []
#masses.append(['H',3.149])
#masses.append(['H2',4.385])
masses.append(['OH',12.4175])
masses.append(['NH3',12.426])
masses.append(['H2O',12.775])

