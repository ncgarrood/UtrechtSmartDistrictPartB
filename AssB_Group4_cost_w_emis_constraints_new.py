# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 16:30:06 2021

@author: NCG
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

#for now setting up just for summer as thinking when we make it a function can specify summer or winter

"""
Parameters value
"""
######## Time-step
Delta_t = 0.25 # 15 minute (0.25 hour) intervals
T=int(24*3*1/Delta_t) #number of time-slots (in three days)

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

"""Question 3 global vairables"""

EMISSION_CONSTRAINTS = np.linspace(12.115126457034332, -14.45707455, num=10) 

def get_minimal_cost(season):
    
    #load either summer or winter input variables
    Ppv = season['PV generation [kW]']
    Pdem = season['Residential load [kW]']
    Celec = season['Electricity price [euro/kWh]']
    Emis = season['Marginal emission factor [kg CO2eq/kWh]']
    
    # Create Model
    m=gp.Model()
    
    # Add Variables
    Pbat_ch = m.addVars(T, lb= 0, ub= Pbatmax, vtype= gp.GRB.CONTINUOUS, name= "Pbat_ch")
    Pbat_dis = m.addVars(T, lb= 0, ub= Pbatmax, vtype= gp.GRB.CONTINUOUS, name= "Pbat_dis")
    
    Pgrid = m.addVars(T, lb= -Pgridmax, ub= Pgridmax, vtype= gp.GRB.CONTINUOUS, name= "Pgrid")
    
    SoC = m.addVars(T, lb= SoC_min, ub= SoC_max, vtype= gp.GRB.CONTINUOUS, name= "SoC")

    # Add Constraints  
    ## Power balance formula
    m.addConstrs(Pgrid[t] + Ppv[t] + Pbat_dis[t] - Pbat_ch[t] == Pdem[t] for t in range(T))      
    ## Battery SoC dynamics constraint 
    m.addConstr(SoC[0] == SoC0)
    m.addConstrs(SoC[t] == SoC[t-1] + ((Pbat_ch[t]*Delta_t*eff_ch)/C_bat) - (Pbat_dis[t]*Delta_t)/(eff_dis*C_bat) for t in range(1,T))
    ## SoC constraints 
    m.addConstrs(SoC_min <= SoC[t] for t in range(T))
    m.addConstrs(SoC_max >= SoC[t] for t in range(T))
    
  

    ## EMMISSIONS CONSTRAINTS - Q3
    df = pd.DataFrame(columns = ['Emissions Constraint', 'Cost', 'Emissions'])
    
    for i in EMISSION_CONSTRAINTS:
        
        m.addConstr((gp.quicksum(Emis[t]*Pgrid[t]*Delta_t for t in range(T))) <= i)
        print(i)
        m.setParam('OutputFlag', 0) # dont print all the gurobi output stuff
        obj = gp.quicksum(Celec[t]*Pgrid[t]*Delta_t for t in range(T)) #for the end units to be in euro need to multiply by deltaT
        m.setObjective(obj, gp.GRB.MINIMIZE)
        m.optimize()
         
        #add the values to the new df
        cost = m.getObjective().getValue()
        emissions = gp.quicksum(Emis[t]*Pgrid[t]*Delta_t for t in range(T)).getValue()
        df.loc[len(df)] = [i, cost, emissions]
    
    return df
                     
get_minimal_cost(summer)