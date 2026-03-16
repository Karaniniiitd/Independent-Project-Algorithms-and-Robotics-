from z3 import *

workers=4
chargers=2
rows=6
cols=6
T=8

opt = Optimize()

cost = [[1.4222109257625242, 1.3789772014701511, 1.2102857904154225, 1.1294583751464817, 1.2556373606843043, 1.2024670687252073, 1.3918992945173863, 1.1516563630394638], [1.238298477076178, 1.2916910197275155, 1.4540564425976676, 1.2523434279086951, 1.140918922199852, 1.377902102078612, 1.309184498337666, 1.1252531706812203], [1.45487312798412, 1.4913927380188265, 1.4051086179982948, 1.4510829752197913, 1.1550737846596664, 1.3649158741300642, 1.4494191439839967, 1.3419919659577206], [1.2360713577263567, 1.050350604034183, 1.2170859177268918, 1.305443486721901, 1.456505526618949, 1.4833031838853794, 1.2385048882763585, 1.43265496388582]]

x0=[Int('x0_'+str(t)) for t in range(T)]
y0=[Int('y0_'+str(t)) for t in range(T)]
b0=[Real('b0_'+str(t)) for t in range(T)]
wait0=[Int('wait0_'+str(t)) for t in range(T)]

x1=[Int('x1_'+str(t)) for t in range(T)]
y1=[Int('y1_'+str(t)) for t in range(T)]
b1=[Real('b1_'+str(t)) for t in range(T)]
wait1=[Int('wait1_'+str(t)) for t in range(T)]

x2=[Int('x2_'+str(t)) for t in range(T)]
y2=[Int('y2_'+str(t)) for t in range(T)]
b2=[Real('b2_'+str(t)) for t in range(T)]
wait2=[Int('wait2_'+str(t)) for t in range(T)]

x3=[Int('x3_'+str(t)) for t in range(T)]
y3=[Int('y3_'+str(t)) for t in range(T)]
b3=[Real('b3_'+str(t)) for t in range(T)]
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

for t in range(T-1):
 opt.add(If(b0[t]<=0, And(x0[t+1]==x0[t], y0[t+1]==y0[t]), True))
 opt.add(If(b1[t]<=0, And(x1[t+1]==x1[t], y1[t+1]==y1[t]), True))
 opt.add(If(b2[t]<=0, And(x2[t+1]==x2[t], y2[t+1]==y2[t]), True))
 opt.add(If(b3[t]<=0, And(x3[t+1]==x3[t], y3[t+1]==y3[t]), True))

for t in range(T):
 opt.add(Implies(assign_0_0[t],And(xc0[t]==x0[t], yc0[t]==y0[t])))
 opt.add(Implies(assign_0_1[t],And(xc1[t]==x0[t], yc1[t]==y0[t])))
 opt.add(Implies(assign_1_0[t],And(xc0[t]==x1[t], yc0[t]==y1[t])))
 opt.add(Implies(assign_1_1[t],And(xc1[t]==x1[t], yc1[t]==y1[t])))
 opt.add(Implies(assign_2_0[t],And(xc0[t]==x2[t], yc0[t]==y2[t])))
 opt.add(Implies(assign_2_1[t],And(xc1[t]==x2[t], yc1[t]==y2[t])))
 opt.add(Implies(assign_3_0[t],And(xc0[t]==x3[t], yc0[t]==y3[t])))
 opt.add(Implies(assign_3_1[t],And(xc1[t]==x3[t], yc1[t]==y3[t])))

for t in range(T):
 opt.add(Sum([If(assign_0_1[t],1,0) for c in range(chargers)])<=1)
 opt.add(Sum([If(assign_1_1[t],1,0) for c in range(chargers)])<=1)
 opt.add(Sum([If(assign_2_1[t],1,0) for c in range(chargers)])<=1)
 opt.add(Sum([If(assign_3_1[t],1,0) for c in range(chargers)])<=1)
 opt.add(Sum([If(assign_3_0[t],1,0) for w in range(workers)])<=1)
 opt.add(Sum([If(assign_3_1[t],1,0) for w in range(workers)])<=1)

for t in range(T):
 opt.add(Implies(assign_0_0[t], b0[t] <= 0))
 opt.add(Implies(assign_0_1[t], b0[t] <= 0))
 opt.add(Implies(assign_1_0[t], b1[t] <= 0))
 opt.add(Implies(assign_1_1[t], b1[t] <= 0))
 opt.add(Implies(assign_2_0[t], b2[t] <= 0))
 opt.add(Implies(assign_2_1[t], b2[t] <= 0))
 opt.add(Implies(assign_3_0[t], b3[t] <= 0))
 opt.add(Implies(assign_3_1[t], b3[t] <= 0))

for t in range(T-1):
 opt.add(b0[t+1]==If(Or(assign_0_0[t],assign_0_1[t]), b0[t]+5, b0[t]-cost[0][t]))
 opt.add(b1[t+1]==If(Or(assign_1_0[t],assign_1_1[t]), b1[t]+5, b1[t]-cost[1][t]))
 opt.add(b2[t+1]==If(Or(assign_2_0[t],assign_2_1[t]), b2[t]+5, b2[t]-cost[2][t]))
 opt.add(b3[t+1]==If(Or(assign_3_0[t],assign_3_1[t]), b3[t]+5, b3[t]-cost[3][t]))

for t in range(T):
 opt.add(wait0[t]==If(And(b0[t]<=0,Not(Or(assign_0_0[t],assign_0_1[t]))),1,0))
 opt.add(wait1[t]==If(And(b1[t]<=0,Not(Or(assign_1_0[t],assign_1_1[t]))),1,0))
 opt.add(wait2[t]==If(And(b2[t]<=0,Not(Or(assign_2_0[t],assign_2_1[t]))),1,0))
 opt.add(wait3[t]==If(And(b3[t]<=0,Not(Or(assign_3_0[t],assign_3_1[t]))),1,0))

total_wait = Sum([Sum(wait0),Sum(wait1),Sum(wait2),Sum(wait3)])
opt.minimize(total_wait)

if opt.check()==sat:
 m=opt.model()
 print("Total wait:",m.evaluate(total_wait))
else:
 print("UNSAT")
