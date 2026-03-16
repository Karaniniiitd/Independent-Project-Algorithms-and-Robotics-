from z3 import *

workers=4
chargers=2
rows=6
cols=6
T=8

opt = Optimize()

x0=[Int('x0_'+str(t)) for t in range(T)]
y0=[Int('y0_'+str(t)) for t in range(T)]
b0=[Int('b0_'+str(t)) for t in range(T)]
wait0=[Int('wait0_'+str(t)) for t in range(T)]

x1=[Int('x1_'+str(t)) for t in range(T)]
y1=[Int('y1_'+str(t)) for t in range(T)]
b1=[Int('b1_'+str(t)) for t in range(T)]
wait1=[Int('wait1_'+str(t)) for t in range(T)]

x2=[Int('x2_'+str(t)) for t in range(T)]
y2=[Int('y2_'+str(t)) for t in range(T)]
b2=[Int('b2_'+str(t)) for t in range(T)]
wait2=[Int('wait2_'+str(t)) for t in range(T)]

x3=[Int('x3_'+str(t)) for t in range(T)]
y3=[Int('y3_'+str(t)) for t in range(T)]
b3=[Int('b3_'+str(t)) for t in range(T)]
wait3=[Int('wait3_'+str(t)) for t in range(T)]

xc0=[Int('xc0_'+str(t)) for t in range(T)]
yc0=[Int('yc0_'+str(t)) for t in range(T)]

xc1=[Int('xc1_'+str(t)) for t in range(T)]
yc1=[Int('yc1_'+str(t)) for t in range(T)]

assign_0_0=[Bool('assign_0_0_'+str(t)) for t in range(T)]
assign_0_1=[Bool('assign_0_1_'+str(t)) for t in range(T)]
assign_1_0=[Bool('assign_1_0_'+str(t)) for t in range(T)]
assign_1_1=[Bool('assign_1_1_'+str(t)) for t in range(T)]
assign_2_0=[Bool('assign_2_0_'+str(t)) for t in range(T)]
assign_2_1=[Bool('assign_2_1_'+str(t)) for t in range(T)]
assign_3_0=[Bool('assign_3_0_'+str(t)) for t in range(T)]
assign_3_1=[Bool('assign_3_1_'+str(t)) for t in range(T)]

opt.add(x0[0]==0)
opt.add(y0[0]==0)
opt.add(b0[0]==2)

opt.add(x1[0]==5)
opt.add(y1[0]==5)
opt.add(b1[0]==2)

opt.add(x2[0]==2)
opt.add(y2[0]==2)
opt.add(b2[0]==1)

opt.add(x3[0]==4)
opt.add(y3[0]==1)
opt.add(b3[0]==1)

opt.add(xc0[0]==1)
opt.add(yc0[0]==1)

opt.add(xc1[0]==5)
opt.add(yc1[0]==2)

for t in range(T):
 opt.add(x0[t]>=0,x0[t]<rows)
 opt.add(y0[t]>=0,y0[t]<cols)
 opt.add(x1[t]>=0,x1[t]<rows)
 opt.add(y1[t]>=0,y1[t]<cols)
 opt.add(x2[t]>=0,x2[t]<rows)
 opt.add(y2[t]>=0,y2[t]<cols)
 opt.add(x3[t]>=0,x3[t]<rows)
 opt.add(y3[t]>=0,y3[t]<cols)
 opt.add(xc0[t]>=0,xc0[t]<rows)
 opt.add(yc0[t]>=0,yc0[t]<cols)
 opt.add(xc1[t]>=0,xc1[t]<rows)
 opt.add(yc1[t]>=0,yc1[t]<cols)

for t in range(T-1):
 opt.add(Abs(x0[t+1]-x0[t])+Abs(y0[t+1]-y0[t])<=1)
 opt.add(Abs(x1[t+1]-x1[t])+Abs(y1[t+1]-y1[t])<=1)
 opt.add(Abs(x2[t+1]-x2[t])+Abs(y2[t+1]-y2[t])<=1)
 opt.add(Abs(x3[t+1]-x3[t])+Abs(y3[t+1]-y3[t])<=1)
 opt.add(Abs(xc0[t+1]-xc0[t])+Abs(yc0[t+1]-yc0[t])<=1)
 opt.add(Abs(xc1[t+1]-xc1[t])+Abs(yc1[t+1]-yc1[t])<=1)

cost=[1 for _ in range(T)]
for t in range(T-1):
 opt.add(b0[t+1]==b0[t]-cost[t]+Sum([If(assign_0_1[t],5,0) for c in range(chargers)]))
 opt.add(b1[t+1]==b1[t]-cost[t]+Sum([If(assign_1_1[t],5,0) for c in range(chargers)]))
 opt.add(b2[t+1]==b2[t]-cost[t]+Sum([If(assign_2_1[t],5,0) for c in range(chargers)]))
 opt.add(b3[t+1]==b3[t]-cost[t]+Sum([If(assign_3_1[t],5,0) for c in range(chargers)]))

for t in range(T):
 opt.add(Implies(assign_0_0[t],And(xc0[t]==x0[t],yc0[t]==y0[t])))
 opt.add(Implies(assign_0_1[t],And(xc1[t]==x0[t],yc1[t]==y0[t])))
 opt.add(Implies(assign_1_0[t],And(xc0[t]==x1[t],yc0[t]==y1[t])))
 opt.add(Implies(assign_1_1[t],And(xc1[t]==x1[t],yc1[t]==y1[t])))
 opt.add(Implies(assign_2_0[t],And(xc0[t]==x2[t],yc0[t]==y2[t])))
 opt.add(Implies(assign_2_1[t],And(xc1[t]==x2[t],yc1[t]==y2[t])))
 opt.add(Implies(assign_3_0[t],And(xc0[t]==x3[t],yc0[t]==y3[t])))
 opt.add(Implies(assign_3_1[t],And(xc1[t]==x3[t],yc1[t]==y3[t])))

for t in range(T):
 opt.add(Sum([If(assign_3_0[t],1,0) for w in range(workers)])<=1)
 opt.add(Sum([If(assign_3_1[t],1,0) for w in range(workers)])<=1)

for t in range(T):
 opt.add(wait0[t]==If(b0[t]<=0,1,0))
 opt.add(wait1[t]==If(b1[t]<=0,1,0))
 opt.add(wait2[t]==If(b2[t]<=0,1,0))
 opt.add(wait3[t]==If(b3[t]<=0,1,0))

total_wait=Sum([Sum(wait0),Sum(wait1),Sum(wait2),Sum(wait3)])
opt.minimize(total_wait)

if opt.check()==sat:
 m=opt.model()
 print('Total wait:',m.evaluate(total_wait))

 print('\nWORKERS')
 print('\nWorker 0')
 for t in range(T):
  print('t',t,'pos',m.evaluate(x0[t]),m.evaluate(y0[t]),'battery',m.evaluate(b0[t]))
 print('\nWorker 1')
 for t in range(T):
  print('t',t,'pos',m.evaluate(x1[t]),m.evaluate(y1[t]),'battery',m.evaluate(b1[t]))
 print('\nWorker 2')
 for t in range(T):
  print('t',t,'pos',m.evaluate(x2[t]),m.evaluate(y2[t]),'battery',m.evaluate(b2[t]))
 print('\nWorker 3')
 for t in range(T):
  print('t',t,'pos',m.evaluate(x3[t]),m.evaluate(y3[t]),'battery',m.evaluate(b3[t]))

 print('\nCHARGERS')
 print('\nCharger 0')
 for t in range(T):
  print('t',t,'pos',m.evaluate(xc0[t]),m.evaluate(yc0[t]))
 print('\nCharger 1')
 for t in range(T):
  print('t',t,'pos',m.evaluate(xc1[t]),m.evaluate(yc1[t]))

 print('\nASSIGNMENTS')
 print('\nWorker 0 charged by Charger 0')
 for t in range(T):
  print('t',t,m.evaluate(assign_0_0[t]))
 print('\nWorker 0 charged by Charger 1')
 for t in range(T):
  print('t',t,m.evaluate(assign_0_1[t]))
 print('\nWorker 1 charged by Charger 0')
 for t in range(T):
  print('t',t,m.evaluate(assign_1_0[t]))
 print('\nWorker 1 charged by Charger 1')
 for t in range(T):
  print('t',t,m.evaluate(assign_1_1[t]))
 print('\nWorker 2 charged by Charger 0')
 for t in range(T):
  print('t',t,m.evaluate(assign_2_0[t]))
 print('\nWorker 2 charged by Charger 1')
 for t in range(T):
  print('t',t,m.evaluate(assign_2_1[t]))
 print('\nWorker 3 charged by Charger 0')
 for t in range(T):
  print('t',t,m.evaluate(assign_3_0[t]))
 print('\nWorker 3 charged by Charger 1')
 for t in range(T):
  print('t',t,m.evaluate(assign_3_1[t]))
