import txaio
txaio.use_asyncio()
from vpython import *

size=1
g=10
t=0
dt=0.001
h=50
e=1                 #恢復係數
re=False            #reset
running=False     
end =False          #shutdown

scene=canvas(title="free fall\n\n",width=600,height=600,x=0,y=0,center=vec(0,h/2,0),background=vec(0,0.6,0.6))
scene.caption="\n"
floor=box(pos=vec(0,0,0),size=vec(40,0.01,10),color=color.blue)
ball=sphere(pos=vec(0,h,0),radius=size,color=color.red,v=vec(0, 0, 0),a=vec(0,-g,0))
gd = graph(title="<i>y</i>-<i>t</i> plot", width=600, height=450, x=0, y=600,
           xtitle="<i>t</i> (s)", ytitle="<i>y</i> (cm)", fast=False)
gd2 = graph(title="<i>v</i>-<i>t</i> plot", width=600, height=450, x=0, y=1050,
            xtitle="<i>t</i> (s)", ytitle="<i>v</i> (cm/s)", fast=False)
yt = gcurve(graph=gd, color=color.red)
vt = gcurve(graph=gd2, color=color.red)

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
    global re,h,running
    ball.pos.y=hslider.value
    ball.v.y =0
    t=0
    yt.delete()
    vt.delete()
    re = False
    running = False
    b1.text = "Run"
    
def stop(b3):
    global end
    end = not end
    
b3 = button(text="Stop Program", pos=scene.title_anchor, bind=stop)
#h滑桿
def seth(hslider):
    ball.pos.y = hslider.value
    htext.text = '{:1.1f} cm'.format(hslider.value)
    
hslider = slider(min=1, max=50, value=15, length=200, bind=seth, right=15,
                 pos=scene.title_anchor,step=1)
htext = wtext(text='{:1.1f} cm'.format(hslider.value), pos=scene.title_anchor)
ball.pos.y = hslider.value

def sete(eslither):
    global e
    e=eslider.value
    etext.text = '{:1.2f}'.format(eslider.value)

eslider=slider(min=0,max=2,value=1,length=200,bind=sete,right=15,pos=scene.title_anchor)
etext=wtext(text='{:1.2f} 恢復係數'.format(eslider.value),pos=scene.title_anchor)

def update():
    global t
    rate(1000)
    ball.pos += ball.v*dt
    ball.v+=ball.a*dt
    yt.plot(pos=(t, ball.pos.y))
    vt.plot(pos=(t, ball.v.y))
    t += dt
#主程式
while not end:
    if ball.pos.y<0:
        ball.pos.y=0
        ball.v=-ball.v*e
    if running: update()
    if re: print("Reset"); init()

print("Stop Program")