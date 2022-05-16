import txaio
txaio.use_asyncio()
from vpython import *

d1 , h1, w1 = 1.8, 0.2, 0.2             # 下方木塊1的長度 = 1.8m, 高度 = 0.2m, 寬度 = 0.2 m
d2 , h2, w2 = 0.2, 0.2, 0.2             # 上方木塊2的長度 = 0.2m, 高度 = 0.2m, 寬度 = 0.2 m
m1, v1, c1 = 0.2, 2.0, color.red        # 下方木塊1的質量 = 0.2 kg, 初速 = 0.0 m/s, 紅色
m2, v2, c2 = 0.1, 0.0, color.green      # 上方木塊2的質量 = 0.1 kg, 初速 = 2.0 m/s, 綠色
xmax, xmin = 3.0, -3.0                  # x 軸範圍
g = 9.8                                 # 重力加速度 = 9.8 m/s^2
mu = 0.5                                # 動摩擦係數
dt = 0.0005     	                
t = 0         	                        
bx = 0      	                        # 計算 b2 初位置用的變數
re=False            #reset
running=False     
end =False          #shutdown

scene = canvas(title="Two Blocks\n\n", width=800, height=300, center=vec(0, 0.4, 0), background=vec(0, 0.6, 0.6))
scene.caption="\n"
floor = box(pos=vec(0, -0.5*h2, 0), size=vec(xmax - xmin, 0.05, 0.8), color=color.blue)

box1 = box(pos=vec(xmin + d1/2, 0, 0), size=vec(d1, h1, w1), color = c1, v=vec(v1, 0, 0))

if(v2 >= v1): bx = xmin + 0.5*d2
else: bx = xmin + d1 - 0.5*d2
box2 = box(pos=vec(bx, h1, 0), size=vec(d2, h2, w2), color=c2, v=vec(v2, 0, 0))

gd = graph(title="<i>E</i> - <i>t</i> plot", x=0, y=300, width=600, height=450, xtitle="<i>t</i> (s)",
           ytitle="red: <i>K</i><sub>1</sub>, green: <i>K</i><sub>2</sub>, blue: <i>E</i> (J)")
kt1 = gcurve(graph=gd, color=c1)
kt2 = gcurve(graph=gd, color=c2)
et = gcurve(graph=gd, color=color.blue)
gd2 = graph(title="<i>v</i> - <i>t</i> plot", x=0, y=750, width=600, height=450, xtitle="<i>t</i> (s)",
            ytitle="red: <i>v</i><sub>1</sub>, green: <i>v</i><sub>2</sub> (m/s)")
vt1 = gcurve(graph=gd2, color=c1)
vt2 = gcurve(graph=gd2, color=c2)

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
    box1.pos=vec(xmin + d1/2, 0, 0)
    if(v2 >= v1): bx = xmin + 0.5*d2
    else: bx = xmin + d1 - 0.5*d2
    box2.pos=vec(bx, h1, 0)
    box1.v=vec(v1, 0, 0)
    box2.v=vec(v2, 0, 0)
    kt1.delete()
    kt2.delete()
    et.delete()
    vt1.delete()
    vt2.delete()
    t=0
    re = False
    running = False
    b1.text = "Run"

def stop(b3):
    global end
    end = not end
    
b3 = button(text="Stop Program", pos=scene.title_anchor, bind=stop)

def setv1(v1input):
    global v1
    v1=v1input.number
    v1text.text = '{:1.1f} m/s(below)'.format(v1)
    init()

v1input=winput(length=200,bind=setv1,right=15,pos=scene.title_anchor,type="numeric")
v1text=wtext(text='{:1.1f} m/s(below)'.format(v1),pos=scene.title_anchor)

def setv2(v2input):
    global v2
    v2=v2input.number
    v2text.text = '{:1.1f} m/s(top)'.format(v2)
    init()

v2input=winput(length=200,bind=setv2,right=15,pos=scene.title_anchor,type="numeric")
v2text=wtext(text='{:1.1f} m/s(top)'.format(v2),pos=scene.title_anchor)

def update():
    global t
    rate(500)
    if(box2.v.x > box1.v.x):
        force = mu * m2 * g
        box1.a = vec(force / m1, 0, 0)
        box2.a = vec(-force / m2, 0, 0)
    elif(box2.v.x < box1.v.x):
        force = mu * m2 * g
        box1.a = vec(-force / m1, 0, 0)
        box2.a = vec(force / m2, 0, 0)
    
    box1.v += box1.a * dt
    box2.v += box2.a * dt
    box1.pos += box1.v * dt
    box2.pos += box2.v * dt
    
    k1 = 0.5 * m1 * mag2(box1.v)
    k2 = 0.5 * m2 * mag2(box2.v)
    e = k1 + k2
    kt1.plot(pos = (t, k1))            
    kt2.plot(pos = (t, k2))
    et.plot(pos = (t, e))

    vt1.plot(pos = (t, box1.v.x))            
    vt2.plot(pos = (t, box2.v.x))
    
    t+=dt
#主程式
while not end:
    if (box1.pos.x > xmax - d1/2) or (box2.pos.x + d2/2 > box1.pos.x + d1/2 + 0.001):
        running=False
    if running: update()
    if re: print("Reset"); init()
