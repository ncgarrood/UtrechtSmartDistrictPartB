# -*- coding: utf-8 -*-
"""
% Energy in the Built Environment
% Assignment 2: Optimal Home Energy Management
% Dr. Tarek AlSkaif

"""
import gurobipy as gp
import csv
import pandas as pd #for csv reading
import numpy as np 
import matplotlib.pyplot as plt #for plotting

"""
Import your input data for the model
"""
summer = pd.read_csv("AssB_Input_Group4_summer.csv")
winter = pd.read_csv("AssB_Input_Group4_winter.csv")

    # dynamic electricity prices vector
    #household's 15-min PV generation vector
    #household's 15-min demand vector


#for now setting up just for summer as thinking when we make it a function can specify summer or winter
Ppv = summer['PV generation [kW]']
Pdem = summer['Residential load [kW]']


"""
Parameters value
"""
######## Time-step
Delta_t = 0.25 # 15 minute (0.25 hour) intervals
T=int(24*3*1/Delta_t) #number of time-slots (in three days)
t=np.linspace(1, T, num=int(T)) 

######## Limits on grid and max, min, and initial SOC
Pgridmax = 3 #[kW]
Pbatmax = 4 #[kW]

SoC_min = 0.2 #[-] (battery min state of charge)
SoC_max = 1 #[-] (battery max state of charge)
SoC0 = 0.5 #[-] (initial battery state of charge at the beginning of the day)

C_bat = 13.5 #battery capacity parameter for a Tesla Powerwall rated at 13,5 [kWh]
eff_dis = 0.94 #battery discharging efficeicny
eff_ch = 0.94 #battery charging efficeicny

######## Plot power demand and PV generation data
f1 = plt.figure(1)

######## other parameters too add?


"""
Step 1: Create a model
"""
m=gp.Model()

"""
Step 2: Define variables
"""
######## Define your decision variables for the time horizon using addVars


# note one parameter is obj = , we have not set it, not sure what it does
Pbat_ch = m.addVars(T, lb= -Pbatmax, ub= Pbatmax, vtype= gp.GRB.CONTINUOUS, name= "Pbat_ch")
Pbat_dis = m.addVars(T, lb= -Pbatmax, ub= Pbatmax, vtype= gp.GRB.CONTINUOUS, name= "Pbat_dis")

Pgrid = m.addVars(T, lb= -Pgridmax, ub= Pgridmax, vtype= gp.GRB.CONTINUOUS, name= "Pgrid")

SoC = m.addVars(T, lb= SoC_min, ub= SoC_max, vtype= gp.GRB.CONTINUOUS, name= "SoC")

    
"""
Step 3: Add constraints
"""
m.addConstrs()

"""
Example 2:
m.addConstrs(p[n,t] <= Pmax[n] for t in range(T) for n in range(N))
m.addConstrs(p[n,t] >= Pmin[n] for t in range(T) for n in range(N))
m.addConstrs(gp.quicksum(p[n,t] for n in range(N)) >= d[t] for t in range(T))

Example 1: 
con1=m.addConstr(x1 + 2*x2 + 3*x3 <= 4)
con2=m.addConstr(x1 + x2 >= 1)

from internet: 
model.addConstrs(x.sum(i, '*') <= capacity[i] for i in range(5))
model.addConstrs(x[i] + x[j] <= 1 for i in range(5) for j in range(5))
model.addConstrs(x[i]*x[i] + y[i]*y[i] <= 1 for i in range(5))
model.addConstrs(x.sum(i, '*') == [0, 2] for i in [1, 2, 4])
model.addConstrs(z[i] == max_(x[i], y[i]) for i in range(5))
model.addConstrs((x[i] == 1) >> (y[i] + z[i] <= 5) for i in range(5))


"""


######## Nonnegative variables - not required since specified in upper/lower bounds of variable definitions
 

    
######## Power balance formula
#mPgrid + Ppv + Pbat_dis == Pdem + Pbat
m.addConstrs((Pgrid[t] + Ppv[t] + Pbat_dis[t] - Pbat_ch == Pdem[t]), for t in range (T)) 
        
######## Battery SoC dynamics constraint 



######## SoC constraints 



######## Power boundaries
    

    
"""
Step 4: Set objective function
"""

m.setObjective()

"""
Step 5: Solve model
"""

m.optimize()

"""
Step 6: Print variables values for optimal solution
""" 
######## Get the values of the decision variables





"""
Step 7: Plot optimal power output from each generator 
"""
######## Plot results
f2 = plt.figure(2)




