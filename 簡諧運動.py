import txaio
txaio.use_asyncio()
from vpython import *

m=4                 # 木塊質量 4 kg
size=1              # 木塊邊長 1 m
R=5                 # 振幅 5 m
k=1                 # 彈性常數 1 N/m
L0=R+size           # 彈簧原長
t =0                # 時間
dt=0.001            # 時間間隔
b=0                 #阻尼
re=False            #reset
running=False     
end =False          #shutdown

scene=canvas(title="Simple Harmonic Motion\n\n", width=800, height=400, x=0, y=0, background=vec(0, 0.6, 0.6))
scene.caption="\n"
floor = box(pos=vec(0, -(size+0.1)/2, 0), size=vec(2*L0, 0.1, R), texture=textures.metal)
wall = box(pos=vec(-L0, 0, 0), size=vec(0.1, size, R), texture=textures.metal)
block = box(pos=vec(R+size/2, 0, 0), size=vec(size, size, size), texture=textures.wood, v=vec(0, 0, 0),m=m)
spring = helix(pos=vec(-L0, 0, 0), radius=0.3*size, thickness=0.05*size, color=color.yellow)
spring.axis = block.pos - spring.pos - vec(size/2, 0, 0)

arrow_v = arrow(pos=block.pos + vec(0, size, 0), axis=vec(0, 0, 0), shaftwidth=0.3*size, color=color.green)
arrow_a = arrow(pos=block.pos + vec(0, 2*size, 0), axis=vec(0, 0, 0), shaftwidth=0.3*size, color=color.magenta)

gd = graph(title="plot", width=600, height=450, x=0, y=400, xtitle="<i>t</i>(s)", 
           ytitle="blue: <i>x</i>(m), green: <i>v</i>(m/s), magenta: <i>a</i>(m/s<sup>2</sup>)")
xt = gcurve(graph=gd, color=color.blue)
vt = gcurve(graph=gd, color=color.green)
at = gcurve(graph=gd, color=color.magenta)

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
    global re,running
    t=0
    block.m=mslider.value
    block.pos.x=R+size/2
    spring.axis=block.pos-spring.pos-vec(size/2,0,0)
    arrow_a.axis=vec(0,0,0)
    arrow_v.axis=vec(0,0,0)
    block.v=vec(0,0,0)
    xt.delete()
    vt.delete()
    at.delete()
    re = False
    running = False
    b1.text = "Run"

def stop(b3):
    global end
    end = not end
    
b3 = button(text="Stop Program", pos=scene.title_anchor, bind=stop)

def setk(kslither):
    global k
    k=kslider.value
    ktext.text = '{:1.1f} 彈性係數'.format(kslider.value)

kslider=slider(min=0.1,max=5,value=1,length=200,bind=setk,right=15,pos=scene.title_anchor)
ktext=wtext(text='{:1.1f} 彈性係數'.format(kslider.value),pos=scene.title_anchor)

def setm(mslither):
    block.m=mslider.value
    mtext.text = '{:1.1f} kg'.format(mslider.value)

mslider=slider(min=0.1,max=10,value=4,length=200,bind=setm,right=15,pos=scene.title_anchor)
mtext=wtext(text='{:1.1f} kg'.format(mslider.value),pos=scene.title_anchor)

def setb(bslither):
    global b,k
    b=bslither.value*sqrt(block.m*k)*2
    btext.text = '{:1.1f}*√4mk 阻尼'.format(bslider.value)

bslider=slider(min=0,max=2,value=0,length=200,bind=setb,right=15,pos=scene.title_anchor,step=0.1)
btext=wtext(text='{:1.1f}*√4mk 阻尼'.format(bslider.value),pos=scene.title_anchor)

def setR(Rslither):
    global R
    R=Rslider.value
    spring.axis=block.pos-spring.pos-vec(size/2,0,0)
    block.pos.x=R+size/2
    init()
    Rtext.text = '{:1.1f} m'.format(Rslider.value)

Rslider=slider(min=1,max=5,value=4,length=200,bind=setR,right=15,pos=scene.title_anchor)
Rtext=wtext(text='{:1.1f} m'.format(Rslider.value),pos=scene.title_anchor)

def update():
    global t
    rate(1000)
    spring.axis= block.pos-spring.pos-vec(0.5*size,0,0)
    F=-k*(spring.axis-vec(L0,0,0))-block.v*b
    block.a=F/block.m
    block.pos+=block.v*dt
    block.v+=block.a*dt
    
    arrow_v.pos=block.pos+vec(0,size,0)
    arrow_a.pos= block.pos+vec(0,2*size,0)
    arrow_v.axis=block.v
    arrow_a.axis=block.a

    xt.plot(pos=(t,block.pos.x-size/2))
    vt.plot(pos=(t,block.v.x))
    at.plot(pos=(t,block.a.x))
    
    t+=dt
#主程式
while not end:
    if running: update()
    if re: print("Reset"); init()