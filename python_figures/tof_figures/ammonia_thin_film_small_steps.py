import MySQLdb

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")

cursor = db.cursor()

initial_db = 403
number_of_spectrums = 57

temperatures = []
for i in range(initial_db,initial_db+number_of_spectrums):
    cursor.execute("select sample_temperature from measurements_tof where id = " + str(i))
    fetch = (cursor.fetchall())
    temperatures = temperatures + [fetch[0][0]]


masses = []
#masses.append(['H2',4.387,8])
masses.append(['OH',12.414,6])
masses.append(['NH3',12.424,6])
masses.append(['H2O',12.770,8])
masses.append(['N2',15.8818,8])
#masses.append(['NO',16.438,10])
masses.append(['O2',16.967,8])
#masses.append(['N2O',19.8699,10])

