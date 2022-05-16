import txaio
txaio.use_asyncio()
from vpython import*

r1 , c1 = 0.1,color.red
r2 , c2 = 0.1, color.green
l, l0, k=1,1,100
t, dt=0, 0.0005
v0=5
re=False            #reset
running=False     
end =False          #shutdown

scene=canvas(title='彈碰\n\n',width=800,height=400,x=0,y=0,background=vec(0,0.6,0.6))
scene.caption="\n"
floor=box(pos=vec(0,-r1,0),size=vec(8*l0,0,r1*4),texture=textures.metal)
cube1=box(pos=vec(-3*l+r1,0,0),size=vec(2*r1,2*r1,2*r1),color=c1,v=vec(v0,0,0),a=vec(0,0,0),m=3)
cube2=box(pos=vec(-0*l,0,0),size=vec(2*r2,2*r2,2*r2),color=c2,v=vec(0,0,0),a=vec(0,0,0),m=3)
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

def run(b1):
    global running
    running=not running
    if running:b1.text="Pause"
    else:b1.text="Run"

b1=button(text="Run",pos=scene.title_anchor,bind=run)

def reset(b2):
    global re
    re = not re
    
b2 = button(text="Reset", pos=scene.title_anchor, bind=reset)
#初始化
def init():
    global t,re,running
    t=0
    spring.axis=vec(0,0,0)
    cube1.pos=vec(-3*l+r1,0,0)
    cube1.v=vec(v0,0,0)
    cube2.pos=vec(0,0,0)
    cube2.v=vec(0,0,0)
    kt1.delete()
    kt2.delete()
    ut.delete()
    et.delete()
    vt1.delete()
    vt2.delete()
    at1.delete()
    at2.delete()
    re = False
    running = False
    b1.text = "Run"

def stop(b3):
    global end
    end = not end
    
b3 = button(text="Stop Program", pos=scene.title_anchor, bind=stop)

def setm1(m1slither):
    cube1.m=m1slider.value
    m1text.text = '{:1.1f} kg(cube1)'.format(m1slider.value)

m1slider=slider(min=0.1,max=5,value=3,length=200,bind=setm1,right=15,pos=scene.title_anchor,step=0.1)
m1text=wtext(text='{:1.1f} kg(cube1)'.format(m1slider.value),pos=scene.title_anchor)

def setm2(m2slither):
    cube2.m=m2slider.value
    m2text.text = '{:1.1f} kg(cube2)'.format(m2slider.value)

m2slider=slider(min=0.1,max=5,value=3,length=200,bind=setm2,right=15,pos=scene.title_anchor,step=0.1)
m2text=wtext(text='{:1.1f} kg(cube2)'.format(m2slider.value),pos=scene.title_anchor)

def setv(vslither):
    v0=vslider.value
    vtext.text = '{:1.1f} m/s'.format(vslider.value)
    init()

vslider=slider(min=0.1,max=5,value=3,length=200,bind=setv,right=15,pos=scene.title_anchor,step=0.1)
vtext=wtext(text='{:1.1f} m/s'.format(m1slider.value),pos=scene.title_anchor)

def update():
    global t
    rate(500)
    tail=cube1.pos+vec(r1,0,0)
    start=cube2.pos-vec(r2,0,0)
    spring.pos=start
    if(mag(start-tail)<l0):
        spring.axis=tail-start
        F=-k*(l0-spring.axis.mag)*spring.axis.norm()
    else:
        spring.axis=vec(-l0,0,0)
        F=vec(0,0,0)
    cube1.a=-F/cube1.m
    cube2.a=F/cube2.m
    cube1.v+=cube1.a*dt
    cube2.v+=cube2.a*dt
    cube1.pos+=cube1.v*dt
    cube2.pos+=cube2.v*dt
    k1=(cube1.m*cube1.v.mag2)/2
    k2=(cube2.m*cube2.v.mag2)/2
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
    
#主程式
while not end:
    if cube2.pos.x>4*l or cube1.pos.x<-4*l:
        running=False
    if running: update()
    if re: print("Reset"); init()
