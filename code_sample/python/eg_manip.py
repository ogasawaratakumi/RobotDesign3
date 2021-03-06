#!/usr/bin/env python

import sys,os,time
from math import atan2,cos,sin,sqrt,degrees,radians

L = 0
L1 = 300
L2 = 250
L3 = 160
L4 = 72


def send_angles(j,wait):
    # with open("./angles.tmp","w") as f:
    with open("/run/shm/angles.tmp","w") as f:
        f.write("%d,%d,%d,%d,%d\n" % (j[0],j[1],j[2],j[3],j[4]))
        f.flush()

    # os.rename("./angles.tmp","./angles")
    os.rename("/run/shm/angles.tmp","/run/shm/angles")
    time.sleep(wait)

def air_toggle(flag,wait):
    # with open("./ev_on_off.tmp","w") as air_f:
    with open("/run/shm/ev_on_off.tmp","w") as air_f:
        air_f.write("1\n" if flag else "0\n")
        air_f.flush()

    # os.rename("./ev_on_off.tmp","./ev_on_off")
    os.rename("/run/shm/ev_on_off.tmp","/run/shm/ev_on_off")
    time.sleep(wait)

def j_k(th1,th2,th3,th4,th5):
    th1,th2,th3,th4,th5 = radians(th1),radians(th2),radians(th3),radians(th4),radians(th5)
    x = cos(th1)*(L2*sin(th2)+L3*sin(th2+th3)+(L4+L)*sin(th2+th3+th4))
    y = sin(th1)*(L2*sin(th2)+L3*sin(th2+th3)+(L4+L)*sin(th2+th3+th4))
    z = L1+L2*cos(th2)+L3*cos(th2+th3)+(L4+L)*cos(th2+th3+th4)
    a = th1
    b = th2+th3+th4
    c = th5
    q = [x,y,z,degrees(a),degrees(b),degrees(c)]
    print(q)
    return q

def i_k(x,y,z,a,b,c):
    th1 = radians(a)
    th5 = radians(c)
    b = radians(b)
    cos3 = (((z-L1-(L4+L)*cos(b))**2+(((x-cos(th1)*(L4+L)*sin(b))**2)+(y-sin(th1)*(L4+L)*sin(b))**2))-L2**2-L3**2)/(2*L3*L2)
    sin3 = (1-cos3**2)**0.5
    th3 = atan2(sin3,cos3)
    cos2 = ((z-L1-(L4+L)*cos(b))*(L2+L3*cos3)+sqrt(((x-cos(th1)*(L4+L)*sin(b))**2)+(y-sin(th1)*(L4+L)*sin(b))**2)*L3*sin3)
    sin2 = (-(z-L1-(L4+L)*cos(b))*L3*sin3+sqrt(((x-cos(th1)*(L4+L)*sin(b))**2)+(y-sin(th1)*(L4+L)*sin(b))**2)*(L2+L3*cos3))
    th2 = atan2(sin2,cos2)
    th4 = b - th2 - th3
    th = [degrees(th1),degrees(th2),degrees(th3),degrees(th4),degrees(th5)] 
    print(th)
    return th

if __name__ == "__main__" :
    air_toggle(True,2.0)
    send_angles(i_k(0,0,L1+L2+L3+L4+L,0,0,-86),3.0)
    send_angles(i_k(269,0,291,0,180,-86),1.0)
    send_angles(i_k(338,0,262,0,140,-86),2.0)
    send_angles(i_k(368,0,250,0,100,-86),2.0)
    send_angles(i_k(389,0,180,0,90,-86),2.0)
    air_toggle(False,2.0)
    send_angles(i_k(395,0,250,0,90,-86),2.0)
    send_angles(i_k(338,0,262,0,90,-86),2.0)
    send_angles(i_k(338,0,262,90,90,-86),2.0)
    send_angles(i_k(395,0,250,90,90,-86),2.0)
    air_toggle(True,2.0)

