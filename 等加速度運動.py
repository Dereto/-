import txaio
txaio.use_asyncio()
from vpython import *

size = 10         
L = 200           
t = 0          
dt = 0.01         
re = False          #reset
running = False     
end = False         #shutdown

scene = canvas(title="1D Motion\n\n", width=800, height=400, x=0, y=0,
               center=vec(0, 5, 0), background=vec(0, 0.6, 0.6))
scene.caption = "\n"
floor = box(pos=vec(0, 0, 0), size=vec(L, 0.1*size, 0.5*L), color=color.blue)
cube = box(pos=vec(0, 0.55*size, 0), size=vec(size, size, size), v=vec(0, 0, 0), color=color.red, a=vec(0,0,0))

gd = graph(title="<i>x</i>-<i>t</i> plot", width=600, height=450, x=0, y=400,
           xtitle="<i>t</i> (s)", ytitle="<i>x</i> (cm)", fast=False)
gd2 = graph(title="<i>v</i>-<i>t</i> plot", width=600, height=450, x=0, y=850,
            xtitle="<i>t</i> (s)", ytitle="<i>v</i> (c  m/s)", fast=False)
gd3 = graph(title="<i>a</i>-<i>t</i> plot", width=600, height=450, x=0, y=1300,
            xtitle="<i>t</i> (s)", ytitle="<i>a</i> (c  m/s^2)", amin=-6.0, amax=6.0, fast=False)
xt = gcurve(graph=gd, color=color.red)
vt = gcurve(graph=gd2, color=color.red)
at = gcurve(graph=gd3, color=color.red)

def run(b1):
    global running
    running = not running
    if running: b1.text = "Pause"
    else: b1.text = "Run"

b1 = button(text="Run", pos=scene.title_anchor, bind=run)

def reset(b2):
    global re
    re = not re
    
b2 = button(text="Reset", pos=scene.title_anchor, bind=reset)

def init():
    global re, running
    cube.pos = vec(0, size*0.55, 0)
    cube.v.x = vslider.value
    cube.a.x = aslider.value
    t = 0
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
#v滑桿
def setv(vslider):
    cube.v.x = vslider.value
    vtext.text = '{:1.1f} cm/s'.format(vslider.value)
    
vslider = slider(min=-5.0, max=5.0, value=1.0, length=200, bind=setv, right=15,
                 pos=scene.title_anchor,step=0.1)
vtext = wtext(text='{:1.1f} cm/s'.format(vslider.value), pos=scene.title_anchor)
cube.v.x = vslider.value
#a滑桿
def seta(aslider):
    cube.a.x = aslider.value
    atext.text = '{:1.1f} cm/s'.format(aslider.value)
    
aslider = slider(min=-5.0, max=5.0, value=1.0, length=200, bind=seta, right=15,
                 pos=scene.title_anchor,step=0.1)
atext = wtext(text='{:1.1f} cm/s^2'.format(aslider.value), pos=scene.title_anchor)
cube.a.x = aslider.value

def update():
    global t
    rate(1000)
    cube.pos += cube.v*dt
    cube.v+=cube.a*dt
    xt.plot(pos=(t, cube.pos.x))
    vt.plot(pos=(t, cube.v.x))
    at.plot(pos=(t, cube.a.x))
    t += dt
#主程式
while not end:
    if (cube.pos.x <= -L*0.5+size*0.5 and cube.v.x < 0) or (cube.pos.x >= L*0.5-size*0.5 and cube.v.x > 0): cube.v.x = 0
    if running: update()
    if re: print("Reset"); init()

print("Stop Program")