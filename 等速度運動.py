from vpython import *

size=0.1
l=1
v=0.03
t=0
dt=0.01

scene =canvas(title="1D motion",width=800,height=600,x=0,y=0,center=vec(0,0.1,0),background=vec(0,0.6,0.6))
floor=box(pos=vec(0,0,0),size=vec(l,0.1*size,0.5*l),color=color.blue)
cube=box(pos=vec(-0.5*l+0.5*size,0.55*size,0),size=vec(size,size,size),color=color.red,v=vec(v,0,0))
gd=graph(title="x-t plot",width=600,height=450,x=0,y=600,xtitle="t(s)",ytitle="x(m)")
gd2=graph(title="v-t plot",width=600,height=450,x=0,y=1050,xtitle="t(s)",ytitle="v(m/s)")
xt=gcurve(graph=gd,color=color.red)
vt=gcurve(graph=gd2,color=color.red)

while(cube.pos.x<=0.5*l-0.5*size):
    rate(500)
    cube.pos.x+=v*dt
    xt.plot(pos=(t,cube.pos.x))
    vt.plot(pos=(t,cube.v.x))
    t+=dt
print("t=",t)
