import txaio
txaio.use_asyncio()
from vpython import *

size=1              # 小球半徑
v0=30               # 小球初速
theta=radians(30)   # 小球抛射仰角
L=100               # 地板長度
g=10                # 重力加速度 9.8 m/s^2
t=0                 
dt=0.001           
re=False            #reset
splash=False
running=False     
end =False          #shutdown

scene = canvas(title="Projection\n\n", width=800, height=400, x=0, y=0,
               center=vec(0, 5, 0), background=vec(0, 0.6, 0.6))
scene.caption="\n"
floor = box(pos=vec(0, -size, 0), size=vec(L, 0.01, 10), texture=textures.metal)
ball = sphere(pos=vec(-L/2, 0, 0), radius=size, color=color.red, make_trail=True,
              v=vec(v0*cos(theta),v0*sin(theta),0), a=vec(0, -g, 0))

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
    ball.pos=vec(-L/2, 0, 0)
    ball.v=vec(v0*cos(theta),v0*sin(theta),0)
    re = False
    running = False
    b1.text = "Run"
    
def stop(b3):
    global end
    end = not end
    
b3 = button(text="Stop Program", pos=scene.title_anchor, bind=stop)

def clear(b4):
    ball.clear_trail()
    
b4 = button(text="clear trail", pos=scene.title_anchor, bind=clear)

def settheta(thetaslither):
    global theta
    theta=radians(thetaslider.value)
    thetatext.text = '{}°'.format(thetaslider.value)
    init()

thetaslider=slider(min=0,max=90,value=30,length=200,bind=settheta,right=15,pos=scene.title_anchor,step=5)
thetatext=wtext(text='{}°'.format(thetaslider.value),pos=scene.title_anchor)

def update():
    global t
    rate(1000)
    ball.pos += ball.v*dt
    ball.v+=ball.a*dt
    t += dt


while not end:
    if ball.pos.y<0:
        running=False
    if running: update()
    if re: print("Reset"); init()
