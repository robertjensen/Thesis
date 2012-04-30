import sys
try:
    import defaults as d
except:
    sys.path.append('../')
    import defaults as d
    
import matplotlib
if 'backend' in locals():
    matplotlib.use(backend)
import matplotlib.pyplot as plt
import numpy as np
import MySQLdb
from scipy import optimize
from scipy import interpolate
import math
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle

matplotlib.rc('text',usetex=True) # Magic fix for the font warnings

try:
    db = MySQLdb.connect(host="servcinf", user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")
except:
    db = MySQLdb.connect(host="127.0.0.1", port=9995, user="cinf_reader",passwd = "cinf_reader", db = "cinfdata")


cursor = db.cursor()