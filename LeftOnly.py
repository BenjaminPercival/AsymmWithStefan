#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 12:05:56 2022

@author: viktor
"""

from z3 import *

X = [ [ Int("x_%s_%s" % (i+1, j+1)) for j in range(12) ] \
      for i in range(2) ]

s=Solver()

RealBCs  = [ Or( X[i][j]==0, X[i][j]==1) \
             for i in range(2) for j in range(12) ]
s.add(RealBCs)

#Scurrent
s.add(And((X[0][0]+X[0][6])%2==0,(X[0][1]+X[0][7])%2==0,(X[0][2]+X[0][8])%2==1,(X[0][3]+X[0][9])%2==1,(X[0][4]+X[0][10])%2==1,(X[0][5]+X[0][11])%2==1))
s.add(And((X[1][0]+X[1][6])%2==1,(X[1][1]+X[1][7])%2==1,(X[1][2]+X[1][8])%2==0,(X[1][3]+X[1][9])%2==0,(X[1][4]+X[1][10])%2==1,(X[1][5]+X[1][11])%2==1))

#dot prod with each other

Prod12=[X[0][j]*X[1][j] for j in range(12)]
DP12=(2+sum(Prod12))/2
s.add(DP12%2==0)

#dot prod with themselves and no real pairing
s.add((sum([X[0][j] for j in range(12)])/2)%4 == 2)
s.add((sum([X[1][j] for j in range(12)])/2)%4 == 2)

countr=0
if s.check() == unsat:
    print("failed to solve")
else:
    while s.check() == sat:
        m = s.model()
        r = [ [ m.evaluate(X[i][j]) for j in range(12) ] 
              for i in range(2) ]
        #print(r)
        countr+=1
        #f = open('BasesA.txt','a') 
    
        #old_stdout = sys.stdout  #  store the default system handler to be able to restore it 
    
        #sys.stdout = f 
        print(countr)
        
        for ls in r:
            
            print(ls)
        #f.close()
        #sys.stdout=old_stdout
        s.add(Not(And([v() == m[v] for v in m]))) 
