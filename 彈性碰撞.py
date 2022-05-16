from vpython import*
r1 , m1, c1 = 0.1, -0.05, color.red
r2 , m2, c2 = 0.1, 0.1, color.green
l, l0, k=0.5,0.5,10
t, dt=0, 0.001
v0=1
scene=canvas(title='彈碰',width=800,height=400,x=0,y=0,background=vec(0,0.6,0.6))
floor=box(pos=vec(0,-r1,0),size=vec(10*l0,0,r1*4),texture=textures.metal)
cube1=box(pos=vec(-3*l+r1,0,0),size=vec(2*r1,2*r1,2*r1),color=c1,v=vec(v0,0,0),a=vec(0,0,0))
cube2=box(pos=vec(-0*l,0,0),size=vec(2*r2,2*r2,2*r2),color=c2,v=vec(0,0,0),a=vec(0,0,0))
spring=helix(pos=cube2.pos-vec(r1,0,0),axis=vec(-l0,0,0),radius=0.3*r1,thickness=0.05*r1,color=color.yellow)
gd = graph(title="E-t plot", x=0, y=300, width=600, height=450, xtitle="<i>t</i> (s)",
           ytitle="red: <i>K</i><sub>1</sub>, green: <i>K</i><sub>2</sub>, orange: <i>U</i>, cyan: <i>E</i> (J)")
kt1 = gcurve(graph=gd, color=c1)
kt2 = gcurve(graph=gd, color=c2)
ut=gcurve(graph=gd,color=color.orange)
et = gcurve(graph=gd, color=color.cyan)

gd2 = graph(title="v-t plot", x=0, y=750, width=600, height=450, xtitle="<i>t</i> (s)",
            ytitle="red: <i>v</i><sub>1</sub>, green: <i>v</i><sub>2</sub> (m/s)")
vt1 = gcurve(graph=gd2, color=c1)
vt2 = gcurve(graph=gd2, color=c2)

gd3 = graph(title="a-t plot", x=0, y=1200, width=600, height=450, xtitle="<i>t</i> (s)",
            ytitle="red: <i>a</i><sub>1</sub>, green: <i>a</i><sub>2</sub> (m/s<sup>2</sup>)")
at1 = gcurve(graph=gd3, color=c1)
at2 = gcurve(graph=gd3, color=c2)
while(cube2.pos.x<=5*l0-r2 and cube1.pos.x>=-5*l0+r1):
    rate(500)
    end=cube1.pos+vec(r1,0,0)
    start=cube2.pos-vec(r2,0,0)
    spring.pos=start
    if(mag(start-end)<l0):
        spring.axis=end-start
        F=-k*(l0-spring.axis.mag)*spring.axis.norm()
    else:
        spring.axis=vec(-l0,0,0)
        F=vec(0,0,0)
    cube1.a=-F/m1
    cube2.a=F/m2
    cube1.v+=cube1.a*dt
    cube2.v+=cube2.a*dt
    cube1.pos+=cube1.v*dt
    cube2.pos+=cube2.v*dt
    k1=(m1*cube1.v.mag2)/2
    k2=(m2*cube2.v.mag2)/2
    u=(k*(l0-spring.axis.mag)**2)/2
    kt1.plot(pos=(t,k1))
    kt2.plot(pos=(t,k2))
    ut.plot(pos=(t,u))
    et.plot(pos=(t,k1+k2+u))
    vt1.plot(pos=(t, cube1.v.x))
    vt2.plot(pos=(t, cube2.v.x))
    at1.plot(pos=(t, cube1.a.x))
    at2.plot(pos=(t, cube2.a.x))
    t+=dt
    
    
