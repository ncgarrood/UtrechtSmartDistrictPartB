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
T=24*3*1/Delta_t #number of time-slots (in three days)
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

######## other parameters we added, N is number of power sources (note batt_ch and batt_disch as seperate)
N = 5

"""
Step 1: Create a model
"""
m=gp.Model()

"""
Step 2: Define variables
"""
######## Define your decision variables for the time horizon using addVars
 
Pgrid = m.AddVar(float(-'inf'), float('inf'), 1, gp.GRB.CONTINUOUS, "Pgrid")

Pbat_ch = m.AddVar(0, float('inf'), 1, gp.GRB.CONTINUOUS, "Pbat_ch")
Pbat_dis = m.AddVar(0, float('inf'), 1, gp.GRB.CONTINUOUS, "Pbat_dis")

SoC = m.AddVar(SoC_min, SoC_max, 1, gp.GRB.CONTINUOUS, "Pbat_ch")
    
 
"""
Step 3: Add constraints
"""

######## Nonnegative variables 
 
    
######## Power balance formula

        
######## Battery SoC dynamics constraint 



######## SoC constraints 



######## Power boundaries
    

    
"""
Step 4: Set objective function
"""



"""
Step 5: Solve model
"""



"""
Step 6: Print variables values for optimal solution
""" 
######## Get the values of the decision variables





"""
Step 7: Plot optimal power output from each generator 
"""
######## Plot results
f2 = plt.figure(2)




