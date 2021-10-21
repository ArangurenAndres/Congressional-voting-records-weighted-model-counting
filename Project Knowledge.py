
"""
Created on Mon Sep 27 16:28:53 2021

@author: sebas
"""

import pandas as pd
import numpy as np
from sympy.logic.boolalg import to_cnf
from sympy.abc import D, R, E, F, G
import os
os.chdir('C:/Users/Andres/Desktop/K project')
cwd = os.getcwd()
data_votes = pd.read_csv('house-votes-84.csv')

#List with the CNF formula, the number of possible outcomes, SAT, notSAT
CNF_formulas = [[to_cnf((D >> E)),2**2,3,1],
                [to_cnf((R >> E)),2**2,3,1],
                [to_cnf((D & E) >> F),2**3,7,1],
                [to_cnf((R & E) >> F),2**3,7,1],
                [to_cnf((F & E) >> D),2**3,7,1],
                [to_cnf((F & E) >> R),2**3,7,1],
                [to_cnf((E >> F)),2**2,3,1],
                [to_cnf((F & E) >> G),2**3,7,1]]

print(CNF_formulas[0])
print(CNF_formulas[1])
print(CNF_formulas[2])
print(CNF_formulas[3])
print(CNF_formulas[4])
print(CNF_formulas[5])
print(CNF_formulas[6])
print(CNF_formulas[7])

# D  = democrat
# R  = republican
# E  = vote1
# F  = vote2
# G  = vote3


print(data_votes.columns)

groupedWeights = data_votes.groupby(by=['Class Name', ' handicapped-infants', ' water-project-cost-sharing',
       ' adoption-of-the-budget-resolution', ' physician-fee-freeze',
       ' el-salvador-aid', ' religious-groups-in-schools',
       ' anti-satellite-test-ban', ' aid-to-nicaraguan-contras', ' mx-missile',
       ' immigration', ' synfuels-corporation-cutback', ' education-spending',
       ' superfund-right-to-sue', ' crime', ' duty-free-exports',
       ' export-administration-act-south-africa']).size().reset_index()

groupedWeights.rename(columns={0:'Weight'}, inplace=True)
len(groupedWeights)

#Based on the formula selected and the mask of the propositions make a column of which row its sat or not
def SelForm(Variable, i):
  if i == 1:
    Formula = (~Variable[0]) | Variable[1]
  elif i ==2:
    Formula = (~Variable[0]) | Variable[1]
  elif i == 3:
    Formula = (~Variable[0]) | (~Variable[1]) | Variable[2]
  elif i == 4:
    Formula = (~Variable[0]) | (~Variable[1]) | Variable[2]
  elif i == 5:
    Formula = (~Variable[1]) | (~Variable[2]) | Variable[0]
  elif i == 6:
    Formula = (~Variable[1]) | (~Variable[2]) | Variable[0]
  elif i == 7:
    Formula = (~Variable[1]) | Variable[2]  
  elif i== 8:
    Formula = (~Variable[1]) | (~Variable[2]) | Variable[3]
  return Formula

#Mask based on the variables of the input its going to assign True or False 
def Mask_Generator(propositions):
    Mask=[]
    for val in propositions:
        if val == 'republican' or val == 'democrat':
            Mask.append(groupedWeights['Class Name'] == val)
        else:
            Mask.append(groupedWeights[val] == 'y')
    return Mask

#Based on the formula and the final column of SelForm select in the dataframe which row are satisfiable
# n is the summatory of the weights in which the formula its true
# d is the summatory of the wights of all the observations
# sat based on the truth table the number of true in the table
# not_sat total observations in the truth table - sat
def Sat_Ex(propositions, formula):
    Cond = Mask_Generator(propositions)
    final_condition = SelForm(Cond, formula)
    df_fil = groupedWeights.loc[final_condition]
    sat = CNF_formulas[formula-1][2]
    n = np.sum(df_fil['Weight'])
    d = np.sum(groupedWeights['Weight'])
    print("SAT")
    print(sat)
    print("n")
    print(n)
    print("d")
    print(d)
    not_sat = CNF_formulas[formula-1][3]
    return np.log((n*not_sat)/((d-n) * sat))




votes = [' handicapped-infants',' water-project-cost-sharing',' adoption-of-the-budget-resolution',' physician-fee-freeze',' el-salvador-aid',' religious-groups-in-schools',' anti-satellite-test-ban',' aid-to-nicaraguan-contras',' mx-missile',' immigration',' synfuels-corporation-cutback',' education-spending',' superfund-right-to-sue',' crime',' duty-free-exports',' export-administration-act-south-africa']

def calFinal(formula,party):
    allWMC = []
    for vote1 in votes:
        for vote2 in votes:
            prop = []
            prop.append(party)
            prop.append(vote1)
            prop.append(vote2)
            prop.append(votes[0])
            FinalR = Sat_Ex(prop, formula)
            allWMC.append([FinalR, party, vote1, vote2])
    allWMC = np.array(allWMC)
    return allWMC


party =  'republican'
Final = calFinal(5,party)

form = 4
prop = []
prop.append(party)
prop.append(' handicapped-infants')
prop.append(' water-project-cost-sharing')
prop.append(votes[0])
Cond = Mask_Generator(prop)
con1 = np.array(Cond)
final_condition = SelForm(Cond, form)
df_fil = groupedWeights.loc[final_condition]
sat = CNF_formulas[form-1][2]
n = np.sum(df_fil['Weight'])
d = np.sum(groupedWeights['Weight'])
print("SAT")
print(sat)
print("n")
print(n)
print("d")
print(d)
not_sat = CNF_formulas[form-1][3]

wmc = np.log((n*not_sat)/((d-n) * sat))


