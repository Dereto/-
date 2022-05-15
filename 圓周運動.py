import txaio
txaio.use_asyncio()
from vpython import *

size = 0.5            # 小球半徑
v0 = 10               # 小球初速
R = 5                 # 圓周運動半徑
L = 5*R               # 地板長度
t = 0                 
dt = 0.001            
re=False            #reset
running=False     
end =False          #shutdown

scene = canvas(title="Circle with Rope\n\n", width=800, height=400, x=0, y=0, background=vec(0, 0.6, 0.6))
scene.caption="\n"
scene.camera.pos = vec(0, L/2, L/2)
scene.camera.axis = vec(0, -L/2, -L/2)
floor = box(pos=vec(0, -size, 0), size=vec(L, 0.01, L), texture=textures.metal)
ball = sphere(pos=vec(R, 0, 0), radius=size, color=color.red, make_trail=True, retain=100, v=vec(0, 0, -v0))
center = cylinder(pos=vec(0, -size, 0), axis=vec(0, 2*size, 0), radius=0.1*size, color=color.white)
rope = cylinder(pos=vec(0, 0, 0), axis=ball.pos, radius=0.1*size, color=color.yellow)
arrow_v = arrow(pos=ball.pos, axis=ball.v, radius=0.2*size, shaftwidth=0.4*size, color=color.green)
arrow_a = arrow(pos=ball.pos, axis=vec(0, 0, 0), radius=0.2*size, shaftwidth=0.4*size, color=color.blue)

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
    ball.pos=vec(R, 0, 0)
    ball.v=vec(0, 0, -v0)
    ball.clear_trail()
    arrow_a.axis=vec(0,0,0)
    arrow_v.axis=ball.v
    arrow_v.pos=ball.pos
    axis = ball.pos
    rope.axis = axis
    re = False
    running = False
    b1.text = "Run"
    
def stop(b3):
    global end
    end = not end
    
b3 = button(text="Stop Program", pos=scene.title_anchor, bind=stop)

def setR(Rslither):
    global R
    R=Rslider.value
    Rtext.text = '{:1.1f} m'.format(Rslider.value)
    init()

Rslider=slider(min=0.1,max=10,value=5,length=200,bind=setR,right=15,pos=scene.title_anchor)
Rtext=wtext(text='{:1.1f} m'.format(Rslider.value),pos=scene.title_anchor)

def setv(vslither):
    global v0
    v0=vslider.value
    vtext.text = '{:1.1f} m/s'.format(vslider.value)
    init()

vslider=slider(min=0,max=15,value=5,length=200,bind=setv,right=15,pos=scene.title_anchor)
vtext=wtext(text='{:1.1f} m/s'.format(vslider.value),pos=scene.title_anchor)

def update():
    global t
    rate(1000)
    axis = ball.pos
    ball.a = -(ball.v.mag2/R)*axis.norm()
    ball.v += ball.a*dt
    ball.pos += ball.v*dt
    rope.axis = axis
    arrow_v.pos = ball.pos
    arrow_v.axis = ball.v
    arrow_a.pos = ball.pos
    arrow_a.axis = ball.a
    t += dt

while not end:
    if running: update()
    if re: print("Reset"); init()